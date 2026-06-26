#!/usr/bin/env node
/**
 * Testet den kompletten Invoice-Flow mit manueller Message-ID
 * 
 * Verwendung:
 * 1. Hole eine echte Message-ID aus deinem Postfach
 * 2. Ersetze TEST_MESSAGE_ID unten
 * 3. Führe das Skript aus
 */

import axios from 'axios';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '../.env') });

// HIER ECHTE MESSAGE-ID EINFÜGEN!
const TEST_MESSAGE_ID = process.env.TEST_MESSAGE_ID || null;

async function testInvoiceFlow() {
  if (!TEST_MESSAGE_ID) {
    console.log('❌ Keine TEST_MESSAGE_ID gesetzt!');
    console.log('\nSo findest du eine Message-ID:');
    console.log('1. Öffne Outlook oder OWA');
    console.log('2. Gehe zu einer Test-Rechnung');
    console.log('3. Kopiere die Message-ID');
    console.log('\nOder setze die Umgebungsvariable:');
    console.log('export TEST_MESSAGE_ID=AAMk...');
    return;
  }
  
  console.log('🧪 Testing Invoice Processing Flow\n');
  console.log('Message ID:', TEST_MESSAGE_ID);
  console.log('Mailbox:', process.env.M365_MAILBOX);
  console.log('\n---\n');
  
  try {
    // Schritt 1: Access Token holen
    console.log('[1/3] Fetching access token...');
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
    
    // Schritt 2: Email Details holen
    console.log('\n[2/3] Fetching email details...');
    const response = await axios.get(
      `https://graph.microsoft.com/v1.0/users/${process.env.M365_MAILBOX}/messages/${TEST_MESSAGE_ID}`,
      { headers: { 'Authorization': `Bearer ${accessToken}` } }
    );
    
    const subject = response.data.subject || '';
    const from = response.data.from?.emailAddress?.address;
    const receivedDateTime = response.data.receivedDateTime;
    
    console.log('✅ Email found:');
    console.log('   Subject:', subject);
    console.log('   From:', from);
    console.log('   Received:', receivedDateTime);
    
    const isInvoice = /rechnung|receipt/i.test(subject);
    console.log('\n   Is Invoice:', isInvoice ? 'YES ✅' : 'NO ❌');
    
    if (!isInvoice) {
      console.log('\n⚠️  This email is NOT an invoice (subject doesn\'t match "Rechnung" or "Receipt")');
      console.log('   Try a different email with "Rechnung" or "Receipt" in the subject');
    }
    
    // Schritt 3: Webhook simulieren
    console.log('\n[3/3] Simulating webhook notification...');
    const WEBHOOK_SECRET = process.env.M365_WEBHOOK_SECRET || 'default-secret';
    const WEBHOOK_URL = 'http://localhost:3000/webhook/m365';
    
    const mockNotification = {
      value: [
        {
          subscriptionId: 'test-subscription-123',
          clientState: WEBHOOK_SECRET,
          changeType: 'created',
          resource: `users/${process.env.M365_MAILBOX}/mailFolders/inbox/messages`,
          resourceData: {
            '@odata.type': '#microsoft.graph.message',
            id: TEST_MESSAGE_ID,
          },
          subscriptionExpirationDateTime: '2026-04-20T11:00:00.0000000Z',
          latestSupportedTlsVersion: 'v1_2',
        },
      ],
    };
    
    const webhookResponse = await axios.post(WEBHOOK_URL, mockNotification, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000, // 30 Sekunden für invoice processing
    });
    
    console.log('\n✅ Webhook sent successfully!');
    console.log('   Status:', webhookResponse.status);
    console.log('   Response:', webhookResponse.data);
    
    console.log('\n📝 Check /tmp/m365-webhook-result.json for processing result');
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    if (error.response) {
      console.error('   Status:', error.response.status);
      if (error.response.data?.error) {
        console.error('   Error:', error.response.data.error.message || error.response.data.error);
      } else {
        console.error('   Data:', JSON.stringify(error.response.data).substring(0, 300));
      }
    }
  }
}

testInvoiceFlow();
