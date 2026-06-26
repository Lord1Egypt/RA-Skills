#!/usr/bin/env node
/**
 * Test Attachment Download
 */

import dotenv from 'dotenv';
import { Client } from '@microsoft/microsoft-graph-client';
import { getAccessToken } from '../src/auth/graph-client.js';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import axios from 'axios';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const rootDir = resolve(__dirname, '../../..');
dotenv.config({ path: resolve(rootDir, '.env'), override: true });

async function testAttachmentDownload() {
  console.log('📎 Testing Attachment Download\n');

  const token = await getAccessToken({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
  });

  const graphClient = Client.init({
    authProvider: (done) => done(null, token),
  });

  const mailbox = process.env.M365_MAILBOX;

  // Find invoice email
  console.log('1️⃣ Finding invoice email...');
  const emails = await graphClient.api(`/users/${mailbox}/messages`)
    .filter('contains(subject, \'Rechnung 6256156\')')
    .select('id,subject,hasAttachments')
    .top(1)
    .get();

  if (emails.value.length === 0) {
    console.log('❌ No invoice email found');
    return;
  }

  const email = emails.value[0];
  console.log(`   Found: ${email.subject}`);
  console.log(`   ID: ${email.id}\n`);

  // Get attachments
  console.log('2️⃣ Getting attachments...');
  const attachments = await graphClient.api(`/users/${mailbox}/messages/${email.id}/attachments`).get();
  
  if (attachments.value.length === 0) {
    console.log('❌ No attachments found');
    return;
  }

  const attachment = attachments.value[0];
  console.log(`   Attachment: ${attachment.name}`);
  console.log(`   Size: ${attachment.size} bytes`);
  console.log(`   Content Type: ${attachment.contentType}\n`);

  // Method 1: Direct $value endpoint with axios
  console.log('3️⃣ Downloading with axios (Method 1)...');
  try {
    const downloadUrl = `https://graph.microsoft.com/v1.0/users/${mailbox}/messages/${email.id}/attachments/${attachment.id}/$value`;
    const response = await axios.get(downloadUrl, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      responseType: 'arraybuffer',
    });
    
    console.log(`   ✅ Downloaded ${response.data.length} bytes`);
    console.log(`   First 20 bytes: ${Buffer.from(response.data).slice(0, 20).toString('hex')}`);
    
    // Check if it's a PDF
    const buffer = Buffer.from(response.data);
    if (buffer.slice(0, 4).toString() === '%PDF') {
      console.log('   ✅ Valid PDF file detected\n');
    }
  } catch (error) {
    console.error(`   ❌ Axios failed: ${error.message}\n`);
  }

  // Method 2: Graph client get()
  console.log('4️⃣ Downloading with Graph client (Method 2)...');
  try {
    const content = await graphClient.api(`/users/${mailbox}/messages/${email.id}/attachments/${attachment.id}/$value`).get();
    console.log(`   Response type: ${typeof content}`);
    console.log(`   Response constructor: ${content?.constructor?.name}`);
    
    if (content instanceof ArrayBuffer) {
      const buffer = Buffer.from(content);
      console.log(`   ✅ Downloaded ${buffer.length} bytes`);
      console.log(`   First 20 bytes: ${buffer.slice(0, 20).toString('hex')}`);
    } else if (Buffer.isBuffer(content)) {
      console.log(`   ✅ Downloaded ${content.length} bytes`);
    } else {
      console.log(`   Content: ${content?.toString()?.substring(0, 100)}`);
    }
  } catch (error) {
    console.error(`   ❌ Graph client failed: ${error.message}\n`);
  }
}

testAttachmentDownload();
