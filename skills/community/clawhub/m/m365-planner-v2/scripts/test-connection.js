#!/usr/bin/env node
/**
 * Test M365 Planner Connection
 * Validates credentials and fetches user info + plans
 */

const { Client } = require('@microsoft/microsoft-graph-client');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Load env from OpenClaw home directory
const envPath = path.join(os.homedir(), '.openclaw', '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
envContent.split('\n').forEach(line => {
    const match = line.match(/^([^#=]+)=(.*)$/);
    if (match) {
        const key = match[1].trim();
        let val = match[2].trim();
        // Remove quotes
        val = val.replace(/^["']|["']$/g, '');
        process.env[key] = val;
    }
});

const clientId = process.env.M365_CLIENT_ID;
const clientSecret = process.env.M365_CLIENT_SECRET;
const tenantId = process.env.M365_TENANT_ID;

async function getAccessToken() {
    const tokenUrl = `https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`;
    
    const params = new URLSearchParams();
    params.append('grant_type', 'client_credentials');
    params.append('client_id', clientId);
    params.append('client_secret', clientSecret);
    params.append('scope', 'https://graph.microsoft.com/.default');

    const response = await axios.post(tokenUrl, params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    return response.data.access_token;
}

async function testConnection() {
    console.log('🔐 M365 Planner Connection Test\n');
    console.log('Client ID:', clientId);
    console.log('Tenant ID:', tenantId);
    console.log('Secret:', clientSecret ? '***' + clientSecret.slice(-4) : 'FEHLT');
    console.log('');

    if (!clientId || !clientSecret || !tenantId) {
        console.error('❌ Fehler: Credentials fehlen in ~/.openclaw/.env');
        process.exit(1);
    }

    try {
        const token = await getAccessToken();
        console.log('✅ Access Token erfolgreich erhalten!\n');

        const client = Client.init({
            authProvider: (done) => done(null, token)
        });

        // Test: Get groups (Planner requires M365 Groups)
        console.log('📋 Test: M365 Groups...');
        const groups = await client.api('/groups').select('id,displayName,mail,resourceProvisioningOptions').top(10).get();
        if (groups.value.length > 0) {
            console.log(`   ${groups.value.length} Gruppen gefunden:\n`);
            groups.value.forEach(g => {
                const isM365 = g.resourceProvisioningOptions?.includes('Team') || g.mail ? '✅ M365/Planner-fähig' : '⚠️ Keine M365-Gruppe';
                console.log(`   - ${g.displayName}`);
                console.log(`     ID: ${g.id}`);
                console.log(`     Mail: ${g.mail || 'N/A'}`);
                console.log(`     Status: ${isM365}\n`);
            });
            console.log('✅ Verbindung erfolgreich! Planner ist bereit.\n');
            console.log('Nächste Schritte:');
            console.log('  1. Wähle eine M365-Gruppe (mit ✅)');
            console.log('  2. Plan in der Gruppe erstellen');
            console.log('  3. Tasks verwalten\n');
        } else {
            console.log('   ❌ Keine Gruppen gefunden');
            console.log('\nErstelle zuerst eine M365-Gruppe im Microsoft 365 Admin Center oder Teams.');
        }

    } catch (error) {
        console.error('❌ Verbindungsfehler:');
        console.error('   Status:', error.response?.status);
        console.error('   Message:', error.message);
        if (error.response?.data?.error) {
            console.error('   Details:', JSON.stringify(error.response.data.error, null, 2));
        }
        process.exit(1);
    }
}

testConnection();
