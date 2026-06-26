#!/usr/bin/env node
/**
 * Send Test Email
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '..', '.env') });

async function sendTestEmail() {
  console.log('📧 Sending Test Email...\n');

  const recipient = process.argv[2] || 'user@domain.com';

  console.log(`To: ${recipient}`);
  console.log(`From: ${process.env.M365_MAILBOX}\n`);

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    mailbox: process.env.M365_MAILBOX,
    enableEmail: true,
  });

  try {
    await client.email.send({
      to: [recipient],
      subject: 'M365 Unified Skill v1.0.0 - Test Email',
      body: `
        <html>
          <body>
            <h2>✅ M365 Unified Skill Test</h2>
            <p>This is a test email from the M365 Unified Skill v1.0.0</p>
            <p><strong>Features tested:</strong></p>
            <ul>
              <li>✅ Email sending via Microsoft Graph API</li>
              <li>✅ OAuth2 Application Authentication</li>
              <li>✅ HTML email formatting</li>
            </ul>
            <p><em>Sent at: ${new Date().toLocaleString('de-DE')}</em></p>
            <hr>
            <p style="color: #666; font-size: 12px;">
              M365 Unified Skill v1.0.0<br>
              MerkelDesign / OpenClaw Community
            </p>
          </body>
        </html>
      `,
      bodyType: 'HTML',
    });

    console.log('✅ Email sent successfully!\n');
    console.log('Check your inbox at:', recipient);

  } catch (error) {
    console.error('❌ Failed to send email:');
    console.error(`   ${error.message}\n`);
    
    if (error.response?.status === 403) {
      console.error('🚫 Permission error:');
      console.error('   Missing: Mail.Send permission');
      console.error('   Add it to your app registration in Azure AD\n');
    }
    
    process.exit(1);
  }
}

sendTestEmail();
