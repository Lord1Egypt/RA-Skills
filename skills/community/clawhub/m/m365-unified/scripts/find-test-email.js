#!/usr/bin/env node
/**
 * Find Test Email
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const rootDir = resolve(__dirname, '../../..');
dotenv.config({ path: resolve(rootDir, '.env'), override: true });

async function findTestEmail() {
  console.log('🔍 Finding Test Email\n');

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    mailbox: process.env.M365_MAILBOX,
    enableEmail: true,
  });

  try {
    // Search for the test email
    const emails = await client.email.search('subject:"Rechnung 6256156"', {
      top: 5,
      select: 'id,subject,isRead,parentFolderId',
    });

    if (emails.length === 0) {
      console.log('❌ Test email not found');
      return;
    }

    const email = emails[0];
    console.log(`✅ Found: ${email.subject}`);
    console.log(`   ID: ${email.id.substring(0, 50)}...`);
    console.log(`   IsRead: ${email.isRead}`);
    console.log(`   ParentFolderId: ${email.parentFolderId}`);
    
    // Get all folders and find which one contains this email
    const folders = await client.folders.list();
    const parentFolder = folders.find(f => email.parentFolderId?.includes(f.id.substring(0, 30)));
    
    if (parentFolder) {
      console.log(`   Location: ${parentFolder.displayName}`);
    } else {
      console.log(`   Location: Unknown (folder ID: ${email.parentFolderId?.substring(0, 30)}...)`);
    }
    console.log('');

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

findTestEmail();
