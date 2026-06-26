#!/usr/bin/env node
/**
 * Test-Skript für M365 Webhook Handler
 * Simuliert eine Webhook-Benachrichtigung und testet die Verarbeitung
 */

import { processNotification } from '../src/webhooks/subscriptions.js';
import axios from 'axios';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '../.env') });

const WEBHOOK_SECRET = process.env.M365_WEBHOOK_SECRET || 'default-secret';

// Mock Notification von Microsoft Graph - PASSE DIESE WERTE AN!
const mockNotification = {
  value: [
    {
      subscriptionId: 'test-subscription-123',
      clientState: WEBHOOK_SECRET,
      changeType: 'created',
      // Teste verschiedene Resource-Pfade
      resource: 'users/user@domain.com/mailFolders/inbox/messages',
      // Alternative Pfade die Microsoft senden könnte:
      // resource: 'users/user@domain.com/messages',
      // resource: '/users/user@domain.com/mailFolders/inbox/messages/AAMk...',
      resourceData: {
        '@odata.type': '#microsoft.graph.message',
        id: 'AAMkAGI2THVSAAA=', // HIER EINE ECHTE MESSAGE-ID FÜR VOLLEN TEST
      },
      subscriptionExpirationDateTime: '2026-04-20T11:00:00.0000000Z',
      latestSupportedTlsVersion: 'v1_2',
    },
  ],
};

console.log('🧪 M365 Webhook Handler Test\n');
console.log('='.repeat(50));
console.log('Mock Notification:', JSON.stringify(mockNotification, null, 2));
console.log('='.repeat(50));

// Erstelle ein Mock-Request-Objekt
const mockReq = {
  body: mockNotification,
  query: {},
};

try {
  console.log('\n[1] Validating notification...');
  const notification = processNotification(mockReq, WEBHOOK_SECRET);
  
  if (!notification) {
    console.error('❌ Notification validation FAILED!');
    console.error('   Possible causes:');
    console.error('   - clientState mismatch');
    console.error('   - Invalid notification format');
    console.error('   - Empty value array');
    process.exit(1);
  }
  
  console.log('✅ Notification validated successfully');
  console.log('\nParsed notification:');
  console.log('   Subscription ID:', notification.subscriptionId);
  console.log('   Changes count:', notification.changes.length);
  
  notification.changes.forEach((change, idx) => {
    console.log(`\n   Change ${idx + 1}:`);
    console.log('     - changeType:', change.changeType);
    console.log('     - resource:', change.resource);
    console.log('     - resourceId:', change.resourceId);
    console.log('     - resourceType:', change.resourceType);
  });
  
  // Teste die Logik aus handleWebhookNotification
  console.log('\n[2] Testing change detection logic...');
  
  if (!notification.changes || notification.changes.length === 0) {
    console.warn('⚠️  WARNING: notification.changes is empty!');
  } else {
    console.log(`✅ Found ${notification.changes.length} change(s)`);
    
    for (const change of notification.changes) {
      console.log('\n--- Analyzing change ---');
      console.log('Resource:', change.resource);
      console.log('ChangeType:', change.changeType);
      
      const resourceLower = (change.resource || '').toLowerCase();
      const isInbox = resourceLower.includes('inbox') || resourceLower.includes('messages');
      const isCreated = change.changeType === 'created';
      
      console.log(`Inbox/Messages: ${isInbox}`);
      console.log(`Created: ${isCreated}`);
      console.log(`Match: ${isInbox && isCreated ? 'YES ✅' : 'NO ❌'}`);
      
      if (isInbox && isCreated) {
        console.log('\n✅ This change would trigger email processing!');
        
        // Optional: Teste fetchEmailDetails wenn eine echte Message-ID vorhanden ist
        if (change.resourceId && change.resourceId !== 'AAMkAGI2THVSAAA=') {
          console.log('\n[3] Testing email fetch (this requires valid credentials)...');
          testFetchEmail(change.resourceId);
        } else {
          console.log('\n⚠️  Skipping email fetch - no valid messageId in mock data');
          console.log('   To test full flow, set a real messageId in the mock notification');
        }
      }
    }
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ Test complete!\n');
  
} catch (error) {
  console.error('\n❌ Error during test:', error.message);
  if (error.response) {
    console.error('   HTTP Status:', error.response.status);
    console.error('   Response:', JSON.stringify(error.response.data).substring(0, 300));
  }
  console.error(error.stack);
  process.exit(1);
}

async function testFetchEmail(messageId) {
  try {
    console.log('Fetching access token...');
    const tokenResponse = await axios.post(
      `https://login.microsoftonline.com/${process.env.M365_TENANT_ID}/oauth2/v2.0/token`,
      new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: process.env.M365_CLIENT_ID,
        client_secret: process.env.M365_CLIENT_SECRET,
        scope: 'https://graph.microsoft.com/.default',
      }),
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    
    console.log('✅ Token received');
    const accessToken = tokenResponse.data.access_token;
    
    console.log(`Fetching message ${messageId}...`);
    const response = await axios.get(
      `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/messages/${messageId}`,
      { headers: { 'Authorization': `Bearer ${accessToken}` } }
    );
    
    console.log('✅ Email fetched successfully!');
    console.log('   Subject:', response.data.subject);
    console.log('   From:', response.data.from?.emailAddress?.address);
    console.log('   Is Invoice:', /rechnung|receipt/i.test(response.data.subject || ''));
    
  } catch (error) {
    console.error('❌ Email fetch failed:', error.message);
    if (error.response) {
      console.error('   Status:', error.response.status);
      console.error('   Data:', error.response.data?.error?.message || JSON.stringify(error.response.data).substring(0, 200));
    }
  }
}
