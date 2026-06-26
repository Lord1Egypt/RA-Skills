#!/usr/bin/env node
/**
 * Test Email Operations
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Load .env from script directory
dotenv.config({ path: path.join(__dirname, '..', '.env') });

async function testEmail() {
  console.log('📧 Testing Email Operations...\n');

  if (!process.env.M365_MAILBOX) {
    console.log('ℹ️  Email not configured - set M365_MAILBOX in .env');
    return;
  }

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    mailbox: process.env.M365_MAILBOX,
    enableEmail: true,
  });

  try {
    // Test 1: List recent emails
    console.log('1️⃣ Listing recent emails in inbox...');
    const messages = await client.email.list({ top: 5, orderBy: 'receivedDateTime desc' });
    console.log(`   Found ${messages.length} messages:\n`);
    messages.forEach(msg => {
      const subject = msg.subject || '(no subject)';
      const from = msg.from?.emailAddress?.address || 'unknown';
      const date = new Date(msg.receivedDateTime).toLocaleDateString();
      console.log(`   📬 ${subject}`);
      console.log(`      From: ${from} | Date: ${date}`);
      console.log('');
    });

    // Test 2: List folders
    console.log('2️⃣ Listing mail folders...');
    const folders = await client.folders.list();
    console.log(`   Found ${folders.length} folders:\n`);
    folders.forEach(folder => {
      console.log(`   📁 ${folder.displayName} (${folder.totalItemCount} items, ${folder.unreadItemCount} unread)`);
    });
    console.log('');

    // Test 3: Search emails (optional)
    console.log('3️⃣ Testing search...');
    const searchResults = await client.email.search('from:notifications', { top: 3 });
    console.log(`   Found ${searchResults.length} matching emails\n`);

    console.log('✅ Email operations test complete!\n');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    if (error.response?.status === 403) {
      console.error('\n🚫 Permission error - MISSING APP PERMISSIONS:');
      console.error('   Go to Azure AD → App registrations → Your app → API permissions');
      console.error('   Add these Application permissions:');
      console.error('   - Mail.Read');
      console.error('   - Mail.ReadWrite');
      console.error('   - Mail.Send');
      console.error('   Then click "Grant admin consent"');
    }
    process.exit(1);
  }
}

testEmail();
