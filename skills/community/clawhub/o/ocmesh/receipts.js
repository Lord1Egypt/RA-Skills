/**
 * receipts.js
 * Delivery and read receipts — the WhatsApp ✓ ✓✓ 🔵 model for agents.
 *
 * - DELIVERED: sent when we successfully decrypt and store a message
 * - READ:      sent when the message is marked as read (via API or agent action)
 */

const { MESSAGE_TYPES, create } = require('./protocol');

let identity = null;
let sendFn = null;

function start(id, messagingSend) {
  identity = id;
  sendFn = messagingSend;
}

async function sendDelivered(toPk, msgId) {
  if (!sendFn) return;
  try {
    await sendFn(toPk, create(MESSAGE_TYPES.DELIVERED, { msgId }));
  } catch (err) {
    console.error('[receipts] Failed to send delivered receipt:', err.message);
  }
}

async function sendRead(toPk, msgId) {
  if (!sendFn) return;
  try {
    await sendFn(toPk, create(MESSAGE_TYPES.READ, { msgId }));
  } catch (err) {
    console.error('[receipts] Failed to send read receipt:', err.message);
  }
}

// Update receipt status in DB when we receive ack from peer
function handleReceipt(db, event, msgContent) {
  const msg = msgContent;
  if (!msg || !msg.msgId) return;

  if (msg.type === MESSAGE_TYPES.DELIVERED) {
    db.prepare('UPDATE messages SET delivered = 1 WHERE id = ?').run(msg.msgId);
    console.log(`[receipts] Delivered ack for ${msg.msgId.slice(0, 12)}...`);
  } else if (msg.type === MESSAGE_TYPES.READ) {
    db.prepare('UPDATE messages SET read_by_peer = 1 WHERE id = ?').run(msg.msgId);
    console.log(`[receipts] Read ack for ${msg.msgId.slice(0, 12)}...`);
  }
}

module.exports = { start, sendDelivered, sendRead, handleReceipt };
