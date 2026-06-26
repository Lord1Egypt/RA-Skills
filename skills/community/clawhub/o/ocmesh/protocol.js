/**
 * protocol.js
 * Typed message schema for ocmesh agent-to-agent communication.
 *
 * All messages are JSON with a required `type` field.
 * Unrecognized types are stored as-is for forward compatibility.
 */

const MESSAGE_TYPES = {
  // Basic
  TEXT:    'text',       // { body: string }
  PING:    'ping',       // {}
  PONG:    'pong',       // {}

  // Agent work
  TASK:    'task',       // { action: string, params: object, replyTo?: string }
  RESULT:  'result',     // { taskId: string, output: any, error?: string }
  ERROR:   'error',      // { code: string, message: string }

  // Social
  INTRO:   'intro',      // { name: string, capabilities: string[] }
  PROFILE: 'profile',    // { name, about, picture, capabilities }

  // Receipts
  DELIVERED: 'delivered', // { msgId: string }
  READ:      'read',      // { msgId: string }

  // Files
  FILE:    'file',       // { name: string, mimeType: string, url: string, size: number }
};

/**
 * Create a typed message payload (JSON string).
 */
function create(type, payload = {}) {
  return JSON.stringify({
    type,
    ts: Date.now(),
    v: '0.2.0',
    ...payload,
  });
}

/**
 * Parse and validate an incoming message string.
 * Returns null if invalid.
 */
function parse(raw) {
  try {
    const msg = typeof raw === 'string' ? JSON.parse(raw) : raw;
    if (!msg.type) return null;
    return msg;
  } catch {
    return null;
  }
}

module.exports = { MESSAGE_TYPES, create, parse };
