const { isLLMStreamResponse, EntropyEngine } = require('./entropy-engine.cjs');
const crypto = require('crypto');

const getOriginalFetch = () => global.__mockFetch || global.__originalFetch || fetch;
if (!global.__originalFetch && typeof fetch !== 'undefined') {
  global.__originalFetch = fetch;
}

const streamRegistry = new Map();
const entropyEngine = new EntropyEngine();

// Periodic cleanup of stale/dead stream contexts (every 30s)
const registryCleanupInterval = setInterval(() => {
  const now = Date.now();
  for (const [id, context] of streamRegistry.entries()) {
    if (context.killed || (now - context.lastActivity > 60000)) {
      context.cleanup();
    }
  }
}, 30000);
registryCleanupInterval.unref();

/**
 * Drop-in fetch replacement that intercepts LLM streaming responses,
 * monitors their entropy, and aborts hallucinating streams.
 */
async function patchedFetch(url, options = {}) {
  const reqSignal = options?.signal;
  const ac = new AbortController();

  if (reqSignal) {
    reqSignal.addEventListener('abort', () => ac.abort(reqSignal.reason), { once: true });
  }

  const modifiedOptions = { ...options, signal: ac.signal };
  let res;
  try {
    res = await getOriginalFetch()(url, modifiedOptions);
  } catch (err) {
    throw err;
  }

  if (!res.body || !isLLMStreamResponse(res)) {
    return res;
  }

  const streamId = crypto.randomUUID();
  const context = {
    streamId,
    accumulatedText: [],
    totalBytes: 0,
    ratio: 0,
    killed: false,
    abortController: ac,
    lastActivity: Date.now(),
    cleanup: () => {
      context.accumulatedText = [];
      streamRegistry.delete(streamId);
    }
  };

  streamRegistry.set(streamId, context);

  const onKill = (ctx, ratio) => {
    try {
      ctx.abortController.abort(new Error('HALLUCINATION_LOOP_DETECTED_BY_ENTROPY_BREAKER'));
    } catch (e) {}
    ctx.cleanup();
  };

  let byteAccumulator = 0;
  let calculationScheduled = false;
  const textDecoder = new TextDecoder('utf-8', { stream: true });

  const webTransform = new TransformStream({
    async transform(chunk, controller) {
      if (context.killed) {
        controller.enqueue(chunk);
        return;
      }

      // Respect backpressure from downstream consumer
      if (controller.desiredSize !== null && controller.desiredSize <= 0) {
        await new Promise(r => setImmediate(r));
      }

      try {
        context.lastActivity = Date.now();
        const text = textDecoder.decode(chunk, { stream: true });
        context.accumulatedText.push(text);
        byteAccumulator += chunk.length;
        context.totalBytes += chunk.length;

        // Schedule entropy check every 1024 bytes (not per-chunk)
        if (byteAccumulator >= 1024 && !calculationScheduled) {
          calculationScheduled = true;
          process.nextTick(async () => {
            calculationScheduled = false;
            byteAccumulator = 0;
            try {
              if (context.totalBytes >= 4000 && !context.killed) {
                const { ratio, isHighlyRepetitive } = await entropyEngine.calculateRatio(context);
                // Hard kill: ratio > 10.0 (pure repetition)
                // Soft kill: ratio > 6.0 + single-char dominance > 50%
                if (ratio > 10.0 || (ratio > 6.0 && isHighlyRepetitive)) {
                  context.killed = true;
                  onKill(context, ratio);
                }
              }
            } catch (err) {
              console.error('[Stream Entropy Breaker] Calculation error:', err.message);
            }
          });
        }
        controller.enqueue(chunk);
      } catch (err) {
        console.error('[Stream Entropy Breaker] Transform error:', err.message);
        context.cleanup();
        controller.enqueue(chunk);
      }
    },
    flush(controller) {
      try {
        const text = textDecoder.decode();
        context.accumulatedText.push(text);
      } catch (e) {}
      context.cleanup();
    }
  });

  const proxiedBody = res.body.pipeThrough(webTransform);

  return new Response(proxiedBody, {
    status: res.status,
    statusText: res.statusText,
    headers: res.headers,
  });
}

function install() {
  if (global.__streamEntropyBreakerInstalled) return;
  if (!global.__originalFetch) global.__originalFetch = fetch;
  global.fetch = patchedFetch;
  global.__streamEntropyBreakerInstalled = true;
}

function uninstall() {
  if (!global.__streamEntropyBreakerInstalled) return;
  global.fetch = global.__originalFetch || fetch;
  delete global.__streamEntropyBreakerInstalled;
}

module.exports = { install, uninstall, patchedFetch };
