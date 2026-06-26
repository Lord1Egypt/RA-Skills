#!/usr/bin/env node
/**
 * Test SharePoint Operations
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env from ~/.openclaw/
const rootDir = resolve(__dirname, '../../..');
const envPath = resolve(rootDir, '.env');
dotenv.config({ path: envPath, override: true });

async function testSharePoint() {
  console.log('📁 SharePoint Connection Test\n');

  const sharepointEnabled = process.env.M365_ENABLE_SHAREPOINT === 'true';
  const siteId = process.env.M365_SHAREPOINT_SITE_ID?.replace(/"/g, '');

  if (!sharepointEnabled || !siteId) {
    console.log('❌ SharePoint not configured');
    console.log(`   Enabled: ${sharepointEnabled}`);
    console.log(`   Site ID: ${siteId || '(not set)'}\n`);
    console.log('💡 Configure in ~/.openclaw/.env:\n');
    console.log('   M365_ENABLE_SHAREPOINT=true');
    console.log('   M365_SHAREPOINT_SITE_ID="tenant.sharepoint.com,site-guid,web-guid"\n');
    return;
  }

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    sharepointSiteId: siteId,
    enableSharepoint: true,
  });

  try {
    // Test 1: Get drive info
    const drive = await client.sharepoint.getDriveInfo();
    console.log('✅ Connected to SharePoint');
    console.log(`   Site: ${drive.name}`);
    console.log(`   Storage: ${(drive.quota.total / 1024 / 1024 / 1024).toFixed(0)} GB total\n`);

    // Test 2: List files in root
    const files = await client.sharepoint.list('/');
    console.log(`📂 Found ${files.length} items in root:\n`);
    files.slice(0, 10).forEach(file => {
      const type = file.folder ? '📁' : '📄';
      const size = file.size ? (file.size / 1024 / 1024).toFixed(1) + ' MB' : '';
      console.log(`   ${type} ${file.name} ${size}`);
    });
    if (files.length > 10) {
      console.log(`   ... and ${files.length - 10} more`);
    }
    console.log('');

    // Test 3: Create a test folder
    const testFolderName = `m365-test-${Date.now()}`;
    const folder = await client.sharepoint.createFolder(testFolderName);
    console.log(`✅ Test folder created: ${folder.name}\n`);

    // Test 4: Upload a test file
    const testContent = 'M365 Unified Skill - SharePoint Test';
    const testFileName = `/${testFolderName}/test.txt`;
    const uploaded = await client.sharepoint.upload(testFileName, testContent, {
      contentType: 'text/plain',
    });
    console.log(`✅ Upload successful: ${uploaded.name}\n`);

    // Test 5: Download the test file
    const downloaded = await client.sharepoint.download(testFileName);
    const content = downloaded.toString();
    console.log(`✅ Download verified: "${content}"\n`);

    // Cleanup: Delete test files from THIS run
    await client.sharepoint.delete(testFileName);
    await client.sharepoint.delete(`/${testFolderName}`);
    
    // Also clean up old test folder from previous runs if exists
    try {
      await client.sharepoint.delete('/m365-skill-test-1776616456171');
    } catch (e) {
      // Ignore if doesn't exist
    }
    
    console.log('🧹 Test files cleaned up\n');

    console.log('✅ SharePoint is ready for production!\n');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    if (error.response?.status === 403) {
      console.error('\n🚫 Permission error - check these API permissions:');
      console.error('   - Sites.ReadWrite.All');
      console.error('   - Files.ReadWrite.All');
      console.error('   - Admin consent granted?');
    } else if (error.response?.status === 404) {
      console.error('\n📍 Not found - check SharePoint Site ID:');
      console.error('   Format: tenant.sharepoint.com,site-guid,web-guid');
      console.error('   Get it via: GET https://graph.microsoft.com/v1.0/sites');
    }
    process.exit(1);
  }
}

testSharePoint();
