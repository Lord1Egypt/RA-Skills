'use strict';

const { execFileSync } = require('child_process');

function send(chatId, message, opts = {}) {
  const args = [
    'message', 'send',
    '--channel', 'telegram',
    '--target', chatId,
    '--message', message,
    '--json'
  ];
  if (opts.buttons) {
    args.push('--buttons', typeof opts.buttons === 'string' ? opts.buttons : JSON.stringify(opts.buttons));
  }
  if (opts.media) {
    args.push('--media', opts.media);
  }

  const result = execFileSync('openclaw', args, {
    encoding: 'utf-8',
    timeout: opts.timeout || 10000
  });

  // Skip CLI noise lines before JSON
  try {
    const jsonStart = result.indexOf('{');
    const jsonStr = jsonStart !== -1 ? result.slice(jsonStart) : result.trim();
    const parsed = JSON.parse(jsonStr);
    return (parsed.payload && parsed.payload.messageId) || parsed.messageId || null;
  } catch (_) {
    return null;
  }
}

function del(chatId, messageId, opts = {}) {
  execFileSync('openclaw', [
    'message', 'delete',
    '--channel', 'telegram',
    '--target', chatId,
    '--message-id', String(messageId)
  ], {
    encoding: 'utf-8',
    timeout: opts.timeout || 10000
  });
}

function replace(chatId, messageId, message, opts = {}) {
  // Send new message first, then delete old one after a short delay.
  const newId = send(chatId, message, opts);
  if (messageId) {
    const { execSync } = require('child_process');
    try { execSync('sleep 1'); } catch (_) {}
    try {
      const r = execFileSync('openclaw', [
        'message', 'delete',
        '--channel', 'telegram',
        '--target', chatId,
        '--message-id', String(messageId),
        '--json'
      ], { encoding: 'utf-8', timeout: 10000 });
      const jsonStart = r.indexOf('{');
      const parsed = jsonStart !== -1 ? JSON.parse(r.slice(jsonStart)) : {};
      const result = parsed.payload || parsed;
      process.stdout.write(JSON.stringify({
        type: 'MARKETPLACE_DELETE_RESULT',
        msgId: messageId,
        ok: result.ok,
        deleted: result.deleted
      }) + '\n');
    } catch (e) {
      process.stdout.write(JSON.stringify({
        type: 'MARKETPLACE_DELETE_RESULT',
        msgId: messageId,
        ok: false,
        error: (e.stdout || e.message || '').slice(0, 200)
      }) + '\n');
    }
  }
  return newId;
}

function edit(chatId, messageId, message, opts = {}) {
  // openclaw message edit does NOT support --buttons.
  // Fall back to replace (delete + send) when buttons present.
  if (opts.buttons) {
    return replace(chatId, messageId, message, opts);
  }

  try {
    const result = execFileSync('openclaw', [
      'message', 'edit',
      '--channel', 'telegram',
      '--target', chatId,
      '--message-id', String(messageId),
      '--message', message,
      '--json'
    ], {
      encoding: 'utf-8',
      timeout: opts.timeout || 10000
    });
    const jsonStart = result.indexOf('{');
    const jsonStr = jsonStart !== -1 ? result.slice(jsonStart) : result.trim();
    const parsed = JSON.parse(jsonStr);
    return parsed.payload?.messageId || parsed.messageId || messageId;
  } catch (_) {
    return null;
  }
}

module.exports = { send, del, replace, edit };
