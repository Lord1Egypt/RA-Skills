#!/usr/bin/env node
/**
 * Reset Test Email - Move back to Posteingang
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const rootDir = resolve(__dirname, '../../..');
dotenv.config({ path: resolve(rootDir, '.env'), override: true });

async function resetTestEmail() {
  console.log('🔄 Resetting Test Email\n');

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    mailbox: process.env.M365_MAILBOX,
    enableEmail: true,
  });

  try {
    // Find the email in 0.1_Rechnungen folder
    const folders = await client.folders.list();
    const rechnungenFolder = folders.find(f => f.displayName === '0.1_Rechnungen');
    
    if (!rechnungenFolder) {
      console.log('ℹ️  0.1_Rechnungen folder not found - email may already be in Posteingang');
      return;
    }

    console.log(`Found folder: ${rechnungenFolder.displayName}`);
    
    // List messages in that folder
    const messages = await client.email.list({ folder: rechnungenFolder.id, top: 10 });
    const testEmail = messages.find(m => m.subject?.includes('6256156'));
    
    if (!testEmail) {
      console.log('ℹ️  Test email not found in 0.1_Rechnungen');
      return;
    }

    console.log(`Found email: ${testEmail.subject}`);
    
    // Find Posteingang
    const inbox = folders.find(f => f.displayName === 'Posteingang');
    if (!inbox) {
      console.log('❌ Posteingang not found!');
      return;
    }

    // Move back to Posteingang
    console.log(`Moving back to Posteingang...`);
    await client.email.move(testEmail.id, inbox.id);
    console.log('✅ Email moved back to Posteingang\n');

    // Also mark as unread
    console.log('Marking as unread...');
    await client.email.markAsUnread(testEmail.id);
    console.log('✅ Email marked as unread\n');

    console.log('📧 Test email is ready for re-processing!\n');

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

resetTestEmail();
