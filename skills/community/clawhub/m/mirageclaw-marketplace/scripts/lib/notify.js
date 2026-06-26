'use strict';

/**
 * Emit a structured JSON event to stdout (OpenClaw forwards `message` to Telegram).
 * Also write a debug line to stderr.
 */
function notify(type, payload = {}) {
  process.stdout.write(JSON.stringify({ type, ts: new Date().toISOString(), ...payload }) + '\n');
  process.stderr.write(`[${type}] ${payload.message || ''}\n`);
}

module.exports = { notify };
