// sender.js v4 — Single-flight, 429-backoff, no duplicate messages
//
// Key design:
//   - backoffUntil: global timestamp, ALL pushes silently dropped until it passes
//   - Single drain loop, no concurrent API calls
//   - edit fail → freeze only, NEVER fallback to sendNew
//   - latest-wins: stale content discarded

const https = require('https');
const { BOT_TOKEN, CHAT_ID } = require('./config');

const MIN_GAP = 4000;  // min ms between API calls

let messageId = null;
let latest = null;
let inflight = false;
let backoffUntil = 0;   // epoch ms — drop all pushes until this time

function tg(method, payload) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(payload);
    const req = https.request({
      hostname: 'api.telegram.org',
      path: `/bot${BOT_TOKEN}/${method}`,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
    }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve(JSON.parse(d)); } catch { resolve({ ok: false }); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

function isBackedOff() {
  return Date.now() < backoffUntil;
}

function pushUpdate(text, forceNew) {
  if (!text) return;
  // Drop during backoff — poll will accumulate, we'll catch up later
  if (isBackedOff()) return;
  if (text.length > 3900) text = text.slice(0, 3900) + '\n…';
  latest = { text, forceNew: forceNew || false };
  if (!inflight) drain();
}

function freezeMessage() {
  messageId = null;
  latest = null;
}

function handleRateLimit(r) {
  const wait = (r.parameters?.retry_after || 30) + 5;
  backoffUntil = Date.now() + wait * 1000;
  console.error(`[sender] 429, backing off ${wait}s until ${new Date(backoffUntil).toISOString()}`);
  // Drop current latest — it's stale by the time backoff ends
  latest = null;
}

async function drain() {
  if (inflight) return;
  inflight = true;

  while (latest) {
    // Check backoff before every send
    if (isBackedOff()) {
      latest = null;
      break;
    }

    const { text, forceNew } = latest;
    latest = null;

    if (forceNew) messageId = null;

    try {
      if (messageId) {
        const r = await tg('editMessageText', {
          chat_id: CHAT_ID, message_id: messageId,
          text, parse_mode: 'HTML', disable_web_page_preview: true,
        });

        if (!r.ok) {
          if (r.error_code === 429) {
            handleRateLimit(r);
            break;
          }
          if (r.description?.includes('not modified')) {
            // identical, skip
          } else {
            console.error('[sender] edit fail, freezing:', (r.description || '').slice(0, 80));
            messageId = null;
            // Do NOT send new — next poll will push naturally
          }
        }
      } else {
        const r = await tg('sendMessage', {
          chat_id: CHAT_ID, text, parse_mode: 'HTML',
          disable_web_page_preview: true, disable_notification: true,
        });

        if (r.ok && r.result) {
          messageId = r.result.message_id;
        } else if (r.error_code === 429) {
          handleRateLimit(r);
          break;
        } else {
          console.error('[sender] send fail:', (r.description || '').slice(0, 80));
        }
      }
    } catch (err) {
      console.error('[sender] error:', err.message);
    }

    await sleep(MIN_GAP);
  }

  inflight = false;
}

module.exports = { pushUpdate, freezeMessage };
