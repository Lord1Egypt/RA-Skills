#!/usr/bin/env node
/**
 * List all Planner Plans and Tasks
 * Usage: node list_plans.js [group-id]
 * If no group-id provided, lists all accessible M365 Groups first
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
const groupId = process.argv[2]; // Optional: Group ID from command line

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

async function listPlans(targetGroupId) {
    const token = await getAccessToken();
    const client = Client.init({ authProvider: (done) => done(null, token) });

    try {
        // If no group ID provided, list all groups first
        if (!targetGroupId) {
            console.log('🔐 M365 Planner - Verfügbare Gruppen\n');
            const groups = await client.api('/groups').select('id,displayName,mail,resourceProvisioningOptions').top(20).get();
            console.log('Wähle eine Gruppe:\n');
            groups.value.forEach(g => {
                const isM365 = g.resourceProvisioningOptions?.includes('Team') || g.mail ? '✅' : '⚠️';
                console.log(`   ${isM365} ${g.displayName}`);
                console.log(`      ID: ${g.id}`);
                console.log(`      Mail: ${g.mail || 'N/A'}\n`);
            });
            console.log('\nUsage: node list_plans.js <group-id>\n');
            return;
        }

        console.log('🔐 M365 Planner - Gruppen-Übersicht\n');
        console.log(`Gruppe ID: ${targetGroupId}\n`);
        console.log('📋 Pläne:\n');
        
        const plans = await client.api(`/groups/${targetGroupId}/planner/plans`).get();

        if (plans.value.length === 0) {
            console.log('   Keine Pläne gefunden.\n');
            return;
        }

        for (const plan of plans.value) {
            console.log(`   📊 Plan: ${plan.title}`);
            console.log(`      ID: ${plan.id}`);
            console.log(`      Created: ${plan.createdDateTime}`);
            console.log('');

            // Get buckets for this plan
            const buckets = await client.api(`/planner/plans/${plan.id}/buckets`).get();
            console.log(`      Buckets (${buckets.value.length}):`);
            buckets.value.forEach(b => {
                console.log(`        - ${b.name} (Order: ${b.orderHint})`);
            });
            console.log('');

            // Get tasks for this plan
            const tasks = await client.api(`/planner/plans/${plan.id}/tasks`).get();
            console.log(`      Tasks (${tasks.value.length}):`);
            
            // Group tasks by bucket
            const tasksByBucket = {};
            buckets.value.forEach(b => { tasksByBucket[b.id] = []; });
            tasks.value.forEach(t => {
                if (tasksByBucket[t.bucketId]) {
                    tasksByBucket[t.bucketId].push(t);
                }
            });

            buckets.value.forEach(b => {
                const bucketTasks = tasksByBucket[b.id];
                if (bucketTasks && bucketTasks.length > 0) {
                    console.log(`        📝 ${b.name}:`);
                    bucketTasks.forEach(t => {
                        const status = t.percentComplete === 100 ? '✅' : t.percentComplete > 0 ? '🔄' : '⏳';
                        console.log(`          ${status} ${t.title} (${t.percentComplete}%)`);
                    });
                }
            });
            console.log('\n   ' + '='.repeat(50) + '\n');
        }

    } catch (error) {
        console.error('❌ Fehler:', error.message);
        if (error.response?.data?.error) {
            console.error('   Details:', JSON.stringify(error.response.data.error, null, 2));
        }
        process.exit(1);
    }
}

// Parse arguments
listPlans(groupId);
