#!/usr/bin/env node
/**
 * Create a new Planner Task
 * Usage: node create_task.js <plan-id> <bucket-id> <title>
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

async function createTask(planId, bucketId, title) {
    console.log('📝 Create Planner Task\n');
    console.log(`Plan ID: ${planId}`);
    console.log(`Bucket ID: ${bucketId}`);
    console.log(`Title: ${title}\n`);

    const token = await getAccessToken();
    const client = Client.init({ authProvider: (done) => done(null, token) });

    try {
        const task = await client.api('/planner/tasks').post({
            planId: planId,
            bucketId: bucketId,
            title: title,
            orderHint: ' !',
            percentComplete: 0
        });

        console.log('✅ Task erfolgreich erstellt!\n');
        console.log(`Task ID: ${task.id}`);
        console.log(`Title: ${task.title}`);
        console.log(`Status: ${task.percentComplete}% complete`);

    } catch (error) {
        console.error('❌ Fehler:', error.message);
        if (error.response?.data?.error) {
            console.error('   Details:', JSON.stringify(error.response.data.error, null, 2));
        }
        process.exit(1);
    }
}

// Parse arguments
const planId = process.argv[2];
const bucketId = process.argv[3];
const title = process.argv.slice(4).join(' ');

if (!planId || !bucketId || !title) {
    console.log('Usage: node create_task.js <plan-id> <bucket-id> <title>');
    console.log('Example: node create_task.js eTDo6vof-0GMLZnILlHR_pcAA3P- 858427945_ "Neue Aufgabe"');
    process.exit(1);
}

createTask(planId, bucketId, title);
