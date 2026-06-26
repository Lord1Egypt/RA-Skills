/**
 * moltpost list [--unread]
 * List inbox messages
 */

import { requireConfig, readActiveInbox } from '../lib/storage.mjs';

export async function cmdList(args) {
  requireConfig();

  const unreadOnly = args.includes('--unread');
  const inbox = readActiveInbox();
  let messages = inbox.messages || [];

  if (unreadOnly) {
    messages = messages.filter((m) => !m.isRead);
  }

  if (messages.length === 0) {
    console.log(unreadOnly ? 'No unread messages.' : 'Inbox is empty.');
    return;
  }

  console.log(`\nInbox (${messages.length} message(s)${unreadOnly ? ', unread only' : ''}):\n`);
  console.log('#    State   From             Time                 Preview');
  console.log('─'.repeat(80));

  messages.forEach((msg, idx) => {
    const num = String(idx + 1).padStart(4);
    const status = msg.isRead ? 'read' : 'unread';
    const from = msg.from.padEnd(16).slice(0, 16);
    const time = new Date(msg.timestamp * 1000)
      .toLocaleString('en-US', { hour12: false })
      .padEnd(20)
      .slice(0, 20);
    const preview = String(msg.content || '').replace(/\n/g, ' ').slice(0, 30);
    const groupTag = msg.group_id ? ` [${msg.group_id}]` : '';
    console.log(`${num}  ${status}  ${from}  ${time}  ${preview}${groupTag}`);
  });

  console.log('');
}
