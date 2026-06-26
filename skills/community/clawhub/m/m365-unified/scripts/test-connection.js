#!/usr/bin/env node
/**
 * Test M365 Unified Connection
 * Validates credentials and shows enabled features
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';

dotenv.config();

async function testConnection() {
  console.log('🔐 M365 Unified Skill - Connection Test\n');
  console.log('Configuration:');
  console.log(`  Tenant ID: ${process.env.M365_TENANT_ID ? '***' + process.env.M365_TENANT_ID.slice(-4) : 'MISSING'}`);
  console.log(`  Client ID: ${process.env.M365_CLIENT_ID ? '***' + process.env.M365_CLIENT_ID.slice(-4) : 'MISSING'}`);
  console.log(`  Client Secret: ${process.env.M365_CLIENT_SECRET ? '***' + process.env.M365_CLIENT_SECRET.slice(-4) : 'MISSING'}`);
  console.log(`  Mailbox: ${process.env.M365_MAILBOX || 'NOT CONFIGURED'}`);
  console.log('');

  // Validate required credentials
  if (!process.env.M365_TENANT_ID || !process.env.M365_CLIENT_ID || !process.env.M365_CLIENT_SECRET) {
    console.error('❌ Missing required credentials in .env:');
    if (!process.env.M365_TENANT_ID) console.error('   - M365_TENANT_ID');
    if (!process.env.M365_CLIENT_ID) console.error('   - M365_CLIENT_ID');
    if (!process.env.M365_CLIENT_SECRET) console.error('   - M365_CLIENT_SECRET');
    console.log('\n📝 Run setup wizard: npm run setup');
    process.exit(1);
  }

  try {
    // Create client with configured features
    const client = await createM365Client({
      tenantId: process.env.M365_TENANT_ID,
      clientId: process.env.M365_CLIENT_ID,
      clientSecret: process.env.M365_CLIENT_SECRET,
      mailbox: process.env.M365_MAILBOX,
      sharedMailboxes: process.env.M365_SHARED_MAILBOXES?.split(',').map(s => s.trim()) || [],
      sharepointSiteId: process.env.M365_SHAREPOINT_SITE_ID,
      onedriveUser: process.env.M365_ONEDRIVE_USER || process.env.M365_MAILBOX,
      plannerGroupId: process.env.M365_PLANNER_GROUP_ID,
      enableEmail: process.env.M365_ENABLE_EMAIL !== 'false',
      enableSharepoint: process.env.M365_ENABLE_SHAREPOINT === 'true',
      enableOnedrive: process.env.M365_ENABLE_ONEDRIVE === 'true',
      enablePlanner: process.env.M365_ENABLE_PLANNER === 'true',
      enableWebhooks: process.env.M365_ENABLE_WEBHOOKS === 'true',
    });

    // Test connection - For app-only auth, we test with a simple API call
    console.log('📡 Connecting to Microsoft Graph...\n');
    
    // Try to get groups (requires Group.Read.All - already needed for Planner)
    const axios = await import('axios');
    const token = await client._token;
    
    try {
      const response = await axios.default.get(
        'https://graph.microsoft.com/v1.0/groups?$top=1',
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      
      console.log('✅ Connection successful!\n');
      console.log('Tenant Info:');
      console.log(`  Groups API: Accessible ✅`);
      console.log(`  Permissions: Group.Read.All (or higher) ✅`);
      console.log('');
    } catch (error) {
      if (error.response?.status === 403) {
        console.error('❌ Permission Error:');
        console.error('   Missing: Group.Read.All');
        console.error('   Add this permission to your app registration\n');
        throw error;
      }
      throw error;
    }

    console.log('Enabled Features:');
    console.log(`  ${process.env.M365_ENABLE_EMAIL !== 'false' && process.env.M365_MAILBOX ? '✓' : '✗'} Email (Exchange Online)`);
    console.log(`  ${process.env.M365_ENABLE_SHAREPOINT === 'true' ? '✓' : '✗'} SharePoint`);
    console.log(`  ${process.env.M365_ENABLE_ONEDRIVE === 'true' ? '✓' : '✗'} OneDrive`);
    console.log(`  ${process.env.M365_ENABLE_PLANNER === 'true' ? '✓' : '✗'} Planner`);
    console.log(`  ${process.env.M365_ENABLE_WEBHOOKS === 'true' ? '✓' : '✗'} Webhooks`);
    console.log('');

    if (process.env.M365_SHARED_MAILBOXES) {
      console.log('Shared Mailboxes:');
      process.env.M365_SHARED_MAILBOXES.split(',').forEach(mb => {
        console.log(`  ✓ ${mb.trim()}`);
      });
      console.log('');
    }

    console.log('✨ M365 Unified Skill is ready!\n');
    console.log('Next Steps:');
    console.log('  - Configure features in .env file');
    console.log('  - Test individual features:');
    if (process.env.M365_ENABLE_EMAIL !== 'false' && process.env.M365_MAILBOX) console.log('      npm run test:email');
    if (process.env.M365_ENABLE_SHAREPOINT === 'true') console.log('      npm run test:sharepoint');
    if (process.env.M365_ENABLE_ONEDRIVE === 'true') console.log('      npm run test:onedrive');
    if (process.env.M365_ENABLE_PLANNER === 'true') console.log('      npm run test:planner');
    console.log('  - Integrate into OpenClaw workflow');
    console.log('');

  } catch (error) {
    console.error('❌ Connection failed:\n');
    console.error(`   ${error.message}\n`);
    
    if (error.response?.status === 401) {
      console.error('🔐 Authentication Error:');
      console.error('   - Check Tenant ID (must be correct UUID)');
      console.error('   - Check Client ID (must be correct UUID)');
      console.error('   - Check Client Secret (not expired, copied correctly)');
      console.error('   - Verify app registration exists in correct tenant\n');
    } else if (error.response?.status === 403) {
      console.error('🚫 Permission Error:');
      console.error('   - API permissions not granted in app registration');
      console.error('   - Admin consent not given');
      console.error('   - Using delegated permissions instead of application permissions');
      console.error('   - Go to Azure AD → App registrations → Your app → API permissions\n');
    } else if (error.response?.status === 404) {
      console.error('📍 Not Found Error:');
      console.error('   - Tenant ID may be incorrect');
      console.error('   - Resource (mailbox/site/group) may not exist');
      console.error('   - Check IDs in .env file\n');
    }

    console.error('💡 Run "npm run setup" to reconfigure the skill.\n');
    process.exit(1);
  }
}

testConnection();
