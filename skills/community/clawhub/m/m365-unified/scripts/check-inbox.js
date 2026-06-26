#!/usr/bin/env node
import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = resolve(__dirname, '../../..');
dotenv.config({ path: resolve(rootDir, '.env'), override: true });

async function checkInbox() {
  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    mailbox: process.env.M365_MAILBOX,
    enableEmail: true,
  });

  // Get Posteingang
  const folders = await client.folders.list();
  const inbox = folders.find(f => f.displayName === 'Posteingang');
  
  console.log(`📥 Posteingang: ${inbox.id.substring(0, 50)}...`);
  console.log(`   Items: ${inbox.totalItemCount}\n`);

  // List recent emails
  const emails = await client.email.list({ top: 10, select: 'subject,isRead,hasAttachments' });
  
  console.log('Recent emails in Posteingang:');
  emails.forEach((e, i) => {
    const status = e.isRead ? '📖' : '📬';
    const att = e.hasAttachments ? '📎' : '  ';
    console.log(`  ${i+1}. ${status} ${att} ${e.subject}`);
  });

  // Find Rechnung 6256156
  const testMail = emails.find(e => e.subject?.includes('6256156'));
  if (testMail) {
    console.log(`\n✅ Found: Rechnung 6256156`);
    console.log(`   Status: ${testMail.isRead ? 'Read' : 'Unread'}`);
    console.log(`   Attachments: ${testMail.hasAttachments ? 'Yes' : 'No'}`);
  }
}

checkInbox();
