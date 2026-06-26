#!/usr/bin/env node
/**
 * Create a new Planner Plan with default buckets
 * Usage: node create_plan.js <plan-name> <group-id>
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

async function createPlan(planName, groupId) {
    console.log('📋 Create Planner Plan\n');
    console.log(`Name: ${planName}`);
    console.log(`Group ID: ${groupId}\n`);

    const token = await getAccessToken();
    const client = Client.init({ authProvider: (done) => done(null, token) });

    try {
        // Create plan
        console.log('Erstelle Plan...');
        const plan = await client.api('/planner/plans').post({
            title: planName,
            owner: groupId,
            createdDateTime: new Date().toISOString()
        });

        console.log(`✅ Plan erstellt: ${plan.id}\n`);

        // Create default buckets
        console.log('Erstelle Standard-Buckets...');
        const buckets = ['To Do', 'In Progress', 'Done'];
        
        for (const name of buckets) {
            const bucket = await client.api('/planner/buckets').post({
                name: name,
                planId: plan.id,
                orderHint: ' !'
            });
            console.log(`   ✅ ${name}`);
        }

        console.log('\n✅ Plan erfolgreich erstellt!\n');
        console.log(`Plan ID: ${plan.id}`);
        console.log('\nNächste Schritte:');
        console.log(`  node scripts/create_task.js ${plan.id} <bucket-id> "Task Title"`);

    } catch (error) {
        console.error('❌ Fehler:', error.message);
        if (error.response?.data?.error) {
            console.error('   Details:', JSON.stringify(error.response.data.error, null, 2));
        }
        process.exit(1);
    }
}

// Parse arguments
const planName = process.argv[2];
const groupId = process.argv[3];

if (!planName || !groupId) {
    console.log('Usage: node create_plan.js <plan-name> <group-id>');
    console.log('Example: node create_plan.js "Project Alpha" abc-123-xyz');
    console.log('\nTip: Use list_plans.js to see available groups.');
    process.exit(1);
}

createPlan(planName, groupId);
