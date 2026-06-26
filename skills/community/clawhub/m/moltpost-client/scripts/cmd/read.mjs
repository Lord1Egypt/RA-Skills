/**
 * moltpost read <id|index>
 * Show message and mark as read
 */

import { requireConfig, readActiveInbox, updateMessage } from '../lib/storage.mjs';

export async function cmdRead(args) {
  requireConfig();

  const target = args[0];
  if (!target) {
    console.error('Usage: moltpost read <message-id-or-index>');
    process.exit(1);
  }

  const inbox = readActiveInbox();
  const messages = inbox.messages || [];

  let msg;
  const num = parseInt(target, 10);
  if (!isNaN(num) && num >= 1 && num <= messages.length) {
    msg = messages[num - 1];
  } else {
    msg = messages.find((m) => m.id === target);
  }

  if (!msg) {
    console.error(`Message not found: ${target}`);
    process.exit(1);
  }

  if (!msg.isRead) {
    updateMessage(msg.id, { isRead: true });
  }

  const time = new Date(msg.timestamp * 1000).toLocaleString('en-US', { hour12: false });
  console.log('\n' + '─'.repeat(60));
  console.log(`Message ID : ${msg.id}`);
  console.log(`From       : ${msg.from}`);
  console.log(`Time       : ${time}`);
  if (msg.group_id) {
    console.log(`Group      : ${msg.group_id}`);
  }
  if (msg.expires_at) {
    const expTime = new Date(msg.expires_at * 1000).toLocaleString('en-US', { hour12: false });
    console.log(`Expires    : ${expTime}`);
  }
  const sigLabel = msg.signature_verified === true ? 'ok' : msg.signature_verified === false ? 'failed' : 'n/a';
  console.log(`Signature  : ${sigLabel}`);
  console.log('─'.repeat(60));
  console.log(msg.content);
  console.log('─'.repeat(60) + '\n');
}
