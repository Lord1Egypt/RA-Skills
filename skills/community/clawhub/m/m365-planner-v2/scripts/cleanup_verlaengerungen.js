#!/usr/bin/env node
/**
 * Cleanup: Delete completed tasks from a specific bucket
 * Usage: node cleanup_verlaengerungen.js <group-id> <plan-name> <bucket-name>
 * Example: node cleanup_verlaengerungen.js abc-123 "My Plan" "Completed Tasks"
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

async function cleanupCompletedTasks(groupId, planName, bucketName) {
    console.log('🧹 Cleanup: Abgeschlossene Tasks löschen\n');
    console.log(`Group ID: ${groupId}`);
    console.log(`Plan: ${planName}`);
    console.log(`Bucket: ${bucketName}\n`);

    const token = await getAccessToken();
    const client = Client.init({ authProvider: (done) => done(null, token) });

    try {
        // Get the plan
        const plans = await client.api(`/groups/${groupId}/planner/plans`).get();
        const plan = plans.value.find(p => p.title === planName);
        
        if (!plan) {
            console.error('❌ Plan nicht gefunden');
            process.exit(1);
        }

        console.log(`Plan: ${plan.title}`);

        // Get buckets
        const buckets = await client.api(`/planner/plans/${plan.id}/buckets`).get();
        const targetBucket = buckets.value.find(b => b.name === bucketName);

        if (!targetBucket) {
            console.error(`❌ Bucket "${bucketName}" nicht gefunden`);
            console.log('Verfügbare Buckets:');
            buckets.value.forEach(b => console.log(`  - ${b.name}`));
            process.exit(1);
        }

        console.log(`Bucket: ${targetBucket.name}\n`);

        // Get all tasks in this bucket
        const tasks = await client.api(`/planner/plans/${plan.id}/tasks`).get();
        const bucketTasks = tasks.value.filter(t => t.bucketId === targetBucket.id);

        console.log(`Tasks im Bucket: ${bucketTasks.length}`);

        // Filter completed tasks (percentComplete === 100)
        const completedTasks = bucketTasks.filter(t => t.percentComplete === 100);
        const openTasks = bucketTasks.filter(t => t.percentComplete < 100);

        console.log(`- Davon erledigt (werden gelöscht): ${completedTasks.length}`);
        console.log(`- Davon offen (bleiben): ${openTasks.length}\n`);

        // Delete completed tasks
        if (completedTasks.length > 0) {
            console.log('🗑️ Lösche erledigte Tasks:\n');
            for (const task of completedTasks) {
                console.log(`   ❌ ${task.title}`);
                // Need to get fresh ETag before delete
                const freshTask = await client.api(`/planner/tasks/${task.id}`).get();
                await client.api(`/planner/tasks/${task.id}`)
                    .headers({ 'If-Match': freshTask['@odata.etag'] })
                    .delete();
            }
            console.log('\n✅ Alle erledigten Tasks gelöscht\n');
        }

        // Show remaining open tasks
        console.log('📋 Verbleibende offene Tasks (jährlich wiederkehrend):\n');
        openTasks.forEach(t => {
            console.log(`   ⏳ ${t.title}`);
        });

        console.log('\n✅ Cleanup abgeschlossen!\n');

    } catch (error) {
        console.error('❌ Fehler:', error.message);
        if (error.response?.data?.error) {
            console.error('   Details:', JSON.stringify(error.response.data.error, null, 2));
        }
        process.exit(1);
    }
}

// Parse arguments
const groupId = process.argv[2];
const planName = process.argv[3];
const bucketName = process.argv[4];

if (!groupId || !planName || !bucketName) {
    console.log('Usage: node cleanup_verlaengerungen.js <group-id> <plan-name> <bucket-name>');
    console.log('Example: node cleanup_verlaengerungen.js abc-123 "My Plan" "Completed Tasks"');
    console.log('\nTip: Use list_plans.js first to see available groups, plans, and buckets.');
    process.exit(1);
}

cleanupCompletedTasks(groupId, planName, bucketName);
