#!/usr/bin/env node
/**
 * Delete a Planner Task (with proper If-Match header)
 * Usage: node delete_task.js <task-id>
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

async function deleteTask(taskId) {
    console.log('🗑️ Delete Planner Task\n');
    console.log(`Task ID: ${taskId}\n`);

    const token = await getAccessToken();
    const client = Client.init({ authProvider: (done) => done(null, token) });

    try {
        // Get task first to retrieve ETag
        console.log('Hole Task für ETag...');
        const task = await client.api(`/planner/tasks/${taskId}`).get();
        console.log(`   Title: ${task.title}`);
        console.log(`   ETag: ${task['@odata.etag']}\n`);

        // Delete with If-Match header
        console.log('Lösche Task...');
        await client.api(`/planner/tasks/${taskId}`)
            .headers({ 'If-Match': task['@odata.etag'] })
            .delete();

        console.log('✅ Task erfolgreich gelöscht!\n');

    } catch (error) {
        console.error('❌ Fehler:', error.message);
        if (error.response?.data?.error) {
            console.error('   Details:', JSON.stringify(error.response.data.error, null, 2));
        }
        process.exit(1);
    }
}

// Parse arguments
const taskId = process.argv[2];

if (!taskId) {
    console.log('Usage: node delete_task.js <task-id>');
    console.log('Example: node delete_task.js abc123xyz');
    process.exit(1);
}

deleteTask(taskId);
