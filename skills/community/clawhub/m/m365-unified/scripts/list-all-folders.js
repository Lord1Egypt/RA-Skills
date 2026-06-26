#!/usr/bin/env node
/**
 * List All Mail Folders with hierarchy
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const rootDir = resolve(__dirname, '../../..');
dotenv.config({ path: resolve(rootDir, '.env'), override: true });

async function listAllFolders() {
  console.log('📂 All Mail Folders\n');

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    mailbox: process.env.M365_MAILBOX,
    enableEmail: true,
  });

  try {
    const folders = await client.folders.list();
    
    console.log('Top-level folders:');
    folders.forEach((f, idx) => {
      console.log(`  ${idx + 1}. ${f.displayName} (${f.totalItemCount || 0} items)`);
    });
    console.log('');

    // Check for our test folders
    const merkelDesign = folders.find(f => f.displayName === '1_MerkelDesign');
    if (merkelDesign) {
      console.log(`\n📁 1_MerkelDesign found!`);
      console.log(`   ID: ${merkelDesign.id}`);
      console.log(`   Items: ${merkelDesign.totalItemCount || 0}`);
      
      // Try to get child folders
      try {
        const details = await client.folders.get(merkelDesign.id);
        console.log(`   Details:`, JSON.stringify(details, null, 2).substring(0, 500));
      } catch (e) {
        console.log(`   Cannot get details: ${e.message}`);
      }
    }

    const rechnungen = folders.find(f => f.displayName === '0.1_Rechnungen');
    if (rechnungen) {
      console.log(`\n📁 0.1_Rechnungen found!`);
      console.log(`   ID: ${rechnungen.id}`);
      console.log(`   Items: ${rechnungen.totalItemCount || 0}`);
    }

    const posteingang = folders.find(f => f.displayName === 'Posteingang');
    if (posteingang) {
      console.log(`\n📥 Posteingang found!`);
      console.log(`   ID: ${posteingang.id}`);
      console.log(`   Items: ${posteingang.totalItemCount || 0}`);
    }

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

listAllFolders();
