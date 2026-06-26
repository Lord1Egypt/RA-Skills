/**
 * moltpost archive
 * Move read messages from active.json to YYYY-MM.jsonl and remove from active
 */

import { requireConfig, readActiveInbox, writeActiveInbox, archiveMessages } from '../lib/storage.mjs';

export async function cmdArchive(args) {
  requireConfig();

  const allFlag = args.includes('--all');
  const inbox = readActiveInbox();
  const messages = inbox.messages || [];

  const toArchive = allFlag
    ? messages
    : messages.filter((m) => m.isRead);

  if (toArchive.length === 0) {
    console.log(allFlag ? 'Inbox is empty; nothing to archive.' : 'No read messages to archive.');
    return;
  }

  archiveMessages(toArchive);

  const archivedIds = new Set(toArchive.map((m) => m.id));
  inbox.messages = messages.filter((m) => !archivedIds.has(m.id));
  writeActiveInbox(inbox);

  console.log(`✓ Archived ${toArchive.length} message(s) to monthly JSONL.`);
  console.log(`  Active inbox now has ${inbox.messages.length} message(s).`);
}
