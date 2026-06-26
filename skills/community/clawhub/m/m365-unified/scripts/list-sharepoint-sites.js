#!/usr/bin/env node
/**
 * List SharePoint Sites
 */

import dotenv from 'dotenv';
import { Client } from '@microsoft/microsoft-graph-client';
import { getAccessToken } from '../src/auth/graph-client.js';

dotenv.config();

async function listSites() {
  console.log('📁 SharePoint Sites suchen...\n');

  try {
    const token = await getAccessToken({
      tenantId: process.env.M365_TENANT_ID,
      clientId: process.env.M365_CLIENT_ID,
      clientSecret: process.env.M365_CLIENT_SECRET,
    });

    const graphClient = Client.init({
      authProvider: (done) => done(null, token),
    });

    console.log('🔍 Suche nach SharePoint Sites...\n');
    
    const sites = await graphClient.api('/sites?search=*')
      .select('id,name,webUrl,displayName')
      .top(20)
      .get();

    console.log('Verfügbare SharePoint Sites:\n');
    console.log('─'.repeat(80));
    
    sites.value?.forEach((site, idx) => {
      console.log(`${idx + 1}. ${site.displayName || site.name}`);
      console.log(`   ID: ${site.id}`);
      console.log(`   URL: ${site.webUrl}`);
      console.log('');
    });

    console.log('─'.repeat(80));
    console.log('\n💡 Um SharePoint zu aktivieren:');
    console.log('   M365_ENABLE_SHAREPOINT=true');
    console.log('   M365_SHAREPOINT_SITE_ID="<tenant>.sharepoint.com,<site-id>,<web-id>"');
    console.log('\n   Die Site-ID hat das Format: tenant.sharepoint.com,xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx,yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy');

  } catch (error) {
    console.error('❌ Fehler:', error.message);
    if (error.response?.status === 403) {
      console.error('\n🚫 Permission error - Sites.Read.All oder Sites.ReadWrite.All benötigt');
    }
    process.exit(1);
  }
}

listSites();
