const zlib = require('zlib');
const { promisify } = require('util');
const deflateAsync = promisify(zlib.deflate);

/**
 * Detects LLM streaming responses by content-type header.
 * Returns true for text/event-stream, application/x-ndjson,
 * or application/stream+json.
 */
function isLLMStreamResponse(response) {
  const contentType = response.headers.get('content-type') || '';
  return (
    contentType.includes('text/event-stream') ||
    contentType.includes('application/x-ndjson') ||
    contentType.includes('application/stream+json')
  );
}

/**
 * Calculates zlib compression ratio to estimate text entropy.
 * High ratio = highly repetitive (low entropy) text.
 * Deduplicates concurrent calculations per streamId.
 */
class EntropyEngine {
  constructor() {
    this.pendingCalculations = new Map();
  }

  calculateRatio(context) {
    const existing = this.pendingCalculations.get(context.streamId);
    if (existing) return existing;

    const promise = this._computeRatio(context).finally(() => {
      this.pendingCalculations.delete(context.streamId);
    });

    this.pendingCalculations.set(context.streamId, promise);
    return promise;
  }

  async _computeRatio(context) {
    let text = context.accumulatedText.join('');

    // Bound memory: keep only the last 4096 chars when text grows large
    if (text.length > 8192) {
      text = text.slice(-4096);
      context.accumulatedText = [text];
    }

    const uncompressed = Buffer.byteLength(text, 'utf8');
    const compressed = await deflateAsync(text, { level: 6, windowBits: 15 });
    const ratio = uncompressed / Math.max(compressed.length, 1);

    // Single-character dominance check (>50% = hallucination pattern)
    let isHighlyRepetitive = false;
    if (text.length > 100) {
      const charCounts = {};
      let maxCount = 0;
      for (let i = 0; i < text.length; i++) {
        const char = text[i];
        charCounts[char] = (charCounts[char] || 0) + 1;
        if (charCounts[char] > maxCount) maxCount = charCounts[char];
      }
      if (maxCount / text.length > 0.5) {
        isHighlyRepetitive = true;
      }
    }

    context.ratio = ratio;
    return { ratio, uncompressed, compressed: compressed.length, isHighlyRepetitive };
  }
}

module.exports = {
  isLLMStreamResponse,
  EntropyEngine
};
