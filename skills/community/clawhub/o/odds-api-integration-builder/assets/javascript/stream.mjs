import { pathToFileURL } from 'node:url';
import { SkillError, baseUrl, createClient, eventId, fail, integer, parseArgs, retryDelay } from './api.mjs';
import { snapshots } from './discovery.mjs';

export async function* readSse(body, onChunk = () => {}) {
  if (!body) throw new SkillError('Stream response has no body.');
  const decoder = new TextDecoder();
  let buffer = '', event = 'message', data = [];
  for await (const chunk of body) {
    onChunk();
    buffer += decoder.decode(chunk, { stream: true });
    if (buffer.length + data.join('\n').length > 2 * 1024 * 1024) throw new SkillError('SSE frame exceeded the client safety cap. Narrow filters.');
    let newline;
    while ((newline = buffer.indexOf('\n')) !== -1) {
      let line = buffer.slice(0, newline); buffer = buffer.slice(newline + 1);
      if (line.endsWith('\r')) line = line.slice(0, -1);
      if (line === '') {
        if (data.length) {
          let payload;
          try { payload = JSON.parse(data.join('\n')); } catch { throw new SkillError('Stream contains an invalid JSON frame.'); }
          if (!payload || typeof payload !== 'object' || Array.isArray(payload)) throw new SkillError('Stream JSON payload must be an object.');
          yield { event, data: payload };
        }
        event = 'message'; data = [];
      } else if (!line.startsWith(':')) {
        const colon = line.indexOf(':');
        const field = colon < 0 ? line : line.slice(0, colon);
        let value = colon < 0 ? '' : line.slice(colon + 1);
        if (value.startsWith(' ')) value = value.slice(1);
        if (field === 'event') event = value;
        if (field === 'data') data.push(value);
      }
    }
  }
  // An unterminated event is discarded; reconnect from the last processed token.
}

export async function runStream({
  id, query = {}, seconds = 60,
  apiKey = process.env.ODDS_API_KEY, base = process.env.ODDS_API_BASE_URL,
  fetchImpl = globalThis.fetch,
  sleep = ms => new Promise(resolve => setTimeout(resolve, ms)),
  emit = frame => console.log(JSON.stringify(frame)), now = Date.now,
}) {
  eventId(id);
  if (Object.keys(query).some(key => !['bookmakers', 'types', 'periods'].includes(key))) throw new SkillError('Unsupported stream filter. Use only bookmakers, types, and periods.');
  const root = baseUrl(base);
  const client = createClient({ apiKey, base: root, fetchImpl, sleep });
  const deadline = now() + seconds * 1000;
  let resume = null, failures = 0, connections = 0;
  while (now() < deadline) {
    if (++connections > 20) throw new SkillError('Stream reconnect budget exhausted. Check upstream health before restarting.');
    if (!resume) {
      const pages = await snapshots(client, id, query);
      resume = pages[0]?.data.resume;
      if (typeof resume !== 'string' || !resume) throw new SkillError('Snapshot is missing a usable resume token.');
      await emit({ event: 'snapshot', data: { event_id: id, pages: pages.map(page => page.data), atomic: pages.length === 1 } });
    }
    if (now() >= deadline) return;
    const url = new URL(`${root}/events/${id}/odds/stream`);
    for (const [key, value] of Object.entries({ ...query, since: resume, catchup: true, heartbeat_sec: 15 })) if (value != null && value !== '') url.searchParams.set(key, String(value));
    const controller = new AbortController();
    const endTimer = setTimeout(() => controller.abort(), Math.max(1, deadline - now()));
    let idleTimer;
    const resetIdle = () => { clearTimeout(idleTimer); idleTimer = setTimeout(() => controller.abort(), 35000); };
    resetIdle();
    let needsResync = false, rateDelay = null;
    try {
      const response = await fetchImpl(url, { headers: { 'X-API-Key': apiKey, Accept: 'text/event-stream' }, redirect: 'error', signal: controller.signal });
      if ([401, 403, 404, 422].includes(response.status)) throw new SkillError(`Stream HTTP ${response.status}. Check authentication, access, event ID, and filters.`);
      if (response.status === 429) {
        rateDelay = retryDelay(response.headers.get('retry-after'), now()) ?? 1000;
        await response.body?.cancel();
        if (rateDelay > 30000) throw new SkillError('Stream rate limit exceeds the retry budget. Retry later.');
      } else if (!response.ok) {
        throw new Error('Retryable stream connection failure');
      } else {
        if (!(response.headers.get('content-type') || '').includes('text/event-stream')) throw new SkillError('Expected an SSE response.');
        for await (const frame of readSse(response.body, resetIdle)) {
          if (frame.data.event_id != null && frame.data.event_id !== id) throw new SkillError('Stream event ID does not match the requested event.');
          if (frame.event === 'resync') {
            await emit(frame); resume = null; needsResync = true; break;
          }
          if (!['delta', 'heartbeat'].includes(frame.event)) continue;
          if (frame.event === 'delta' && (!Array.isArray(frame.data.changes) || typeof frame.data.resume !== 'string' || !frame.data.resume)) throw new SkillError('Delta is missing changes or a resume token.');
          await emit(frame);
          if (frame.event === 'delta') resume = frame.data.resume;
          failures = 0;
        }
      }
    } catch (error) {
      if (error instanceof SkillError) throw error;
      if (now() >= deadline) return;
      // A finite read consumer can safely replay frames after a connection failure.
    } finally {
      clearTimeout(endTimer); clearTimeout(idleTimer); controller.abort();
    }
    if (now() >= deadline) return;
    if (!needsResync && ++failures > 5) throw new SkillError('Stream retries exhausted. Retry later from a fresh snapshot.');
    const wait = rateDelay ?? (needsResync ? 250 : Math.min(20000, 500 * 2 ** failures));
    await sleep(Math.min(wait, Math.max(0, deadline - now())));
  }
}

export async function main(argv = process.argv.slice(2)) {
  const { command, options: o } = parseArgs(argv, ['event-id', 'bookmakers', 'types', 'periods', 'seconds']);
  if (o.help) { console.log('Finite odds SSE consumer — Node.js 22+\n\nnode stream.mjs --event-id ID [--bookmakers KEYS] [--types TYPES] [--periods LABELS] [--seconds 60]\n\nEmits JSON lines. Reads ODDS_API_KEY at runtime. No background job or cache is created.'); return; }
  if (command) throw new SkillError('Use --event-id; no positional command is supported.');
  await runStream({ id: o['event-id'], query: { bookmakers: o.bookmakers, types: o.types, periods: o.periods }, seconds: integer(o.seconds, 60, 1, 3600, '--seconds') });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main().catch(fail);
