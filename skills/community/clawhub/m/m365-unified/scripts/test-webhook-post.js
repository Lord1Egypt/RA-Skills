#!/usr/bin/env node
/**
 * Sendet einen echten POST-Request an den laufenden Webhook Handler
 */

import axios from 'axios';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '../.env') });

const WEBHOOK_SECRET = process.env.M365_WEBHOOK_SECRET || 'default-secret';
const WEBHOOK_URL = 'http://localhost:3000/webhook/m365';

// Mock Notification von Microsoft Graph
const mockNotification = {
  value: [
    {
      subscriptionId: 'test-subscription-123',
      clientState: WEBHOOK_SECRET,
      changeType: 'created',
      resource: 'users/user@domain.com/mailFolders/inbox/messages',
      resourceData: {
        '@odata.type': '#microsoft.graph.message',
        id: 'AAMkAGI2THVSAAA=', // Mock ID - wird nicht wirklich gefetcht
      },
      subscriptionExpirationDateTime: '2026-04-20T11:00:00.0000000Z',
      latestSupportedTlsVersion: 'v1_2',
    },
  ],
};

async function sendWebhook() {
  console.log('📡 Sending webhook to:', WEBHOOK_URL);
  console.log('Payload:', JSON.stringify(mockNotification, null, 2));
  console.log('\n---\n');
  
  try {
    const response = await axios.post(WEBHOOK_URL, mockNotification, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 10000,
    });
    
    console.log('\n✅ Response received!');
    console.log('Status:', response.status);
    console.log('Data:', response.data);
    
  } catch (error) {
    console.error('\n❌ Request failed:', error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Data:', error.response.data);
    } else if (error.request) {
      console.error('No response received - check if handler is running');
    }
  }
}

sendWebhook();
