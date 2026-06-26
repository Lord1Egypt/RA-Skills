#!/usr/bin/env node
/**
 * Prepare Test Email - Move to Posteingang and mark as unread
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const rootDir = resolve(__dirname, '../../..');
dotenv.config({ path: resolve(rootDir, '.env'), override: true });

async function prepareTestEmail() {
  console.log('📧 Preparing Test Email\n');

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    mailbox: process.env.M365_MAILBOX,
    enableEmail: true,
  });

  try {
    // Find the test email
    const emails = await client.email.search('subject:"Rechnung 6256156"', {
      top: 1,
      select: 'id,subject,isRead',
    });

    if (emails.length === 0) {
      console.log('❌ Test email not found');
      return;
    }

    const email = emails[0];
    console.log(`Found: ${email.subject}`);
    console.log(`Current status: ${email.isRead ? 'Read' : 'Unread'}\n`);

    // Get Posteingang
    const folders = await client.folders.list();
    const inbox = folders.find(f => f.displayName === 'Posteingang');
    
    if (!inbox) {
      console.log('❌ Posteingang not found!');
      return;
    }

    // Move to Posteingang
    console.log('Moving to Posteingang...');
    await client.email.move(email.id, inbox.id);
    console.log('✅ Moved to Posteingang\n');

    // Mark as unread
    console.log('Marking as unread...');
    await client.email.markAsUnread(email.id);
    console.log('✅ Marked as unread\n');

    console.log('📧 Test email is ready for processing!\n');
    console.log('   Location: Posteingang');
    console.log('   Status: Unread');
    console.log('   Subject: Rechnung 6256156\n');

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

prepareTestEmail();
