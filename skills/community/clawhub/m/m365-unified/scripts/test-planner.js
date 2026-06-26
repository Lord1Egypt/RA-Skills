#!/usr/bin/env node
/**
 * Test Planner Operations
 */

import dotenv from 'dotenv';
import { createM365Client } from '../src/index.js';

dotenv.config();

async function testPlanner() {
  console.log('📋 Testing Planner Operations...\n');

  if (!process.env.M365_PLANNER_GROUP_ID) {
    console.log('ℹ️  Planner not configured - set M365_PLANNER_GROUP_ID in .env');
    console.log('   Get Group ID via:');
    console.log('   GET https://graph.microsoft.com/v1.0/groups?$filter=resourceProvisioningOptions/Any(x:x eq \'Team\')\n');
    return;
  }

  const client = await createM365Client({
    tenantId: process.env.M365_TENANT_ID,
    clientId: process.env.M365_CLIENT_ID,
    clientSecret: process.env.M365_CLIENT_SECRET,
    plannerGroupId: process.env.M365_PLANNER_GROUP_ID,
    enablePlanner: true,
  });

  try {
    // Test 1: List plans
    console.log('1️⃣ Listing Planner plans...');
    const plans = await client.planner.listPlans();
    
    if (plans.length === 0) {
      console.log('   ℹ️  No plans found in this group');
      console.log('   Create a plan first in Microsoft Planner web UI\n');
    } else {
      console.log(`   Found ${plans.length} plan(s):\n`);
      plans.forEach(plan => {
        console.log(`   📋 ${plan.title}`);
        console.log(`      ID: ${plan.id}`);
        console.log(`      Created: ${new Date(plan.createdDateTime).toLocaleDateString()}\n`);
      });

      // Test 2: List tasks in first plan
      if (plans.length > 0) {
        console.log('2️⃣ Listing tasks in first plan...');
        const tasks = await client.planner.listTasks(plans[0].id);
        console.log(`   Found ${tasks.length} task(s):\n`);
        tasks.slice(0, 5).forEach(task => {
          const status = task.percentComplete === 100 ? '✅' : task.percentComplete > 0 ? '🔄' : '⏳';
          console.log(`   ${status} ${task.title}`);
          console.log(`      Priority: ${task.priority} | Progress: ${task.percentComplete}%`);
          if (task.dueDateTime) {
            console.log(`      Due: ${new Date(task.dueDateTime).toLocaleDateString()}`);
          }
          console.log('');
        });

        // Test 3: List buckets
        console.log('3️⃣ Listing buckets...');
        const buckets = await client.planner.listBuckets(plans[0].id);
        console.log(`   Found ${buckets.length} bucket(s):\n`);
        buckets.forEach(bucket => {
          console.log(`   🗂️  ${bucket.name}`);
        });
        console.log('');
      }
    }

    // Test 4: Create a test task (optional - commented out by default)
    /*
    console.log('4️⃣ Creating test task...');
    const testTask = await client.planner.createTask(plans[0].id, 'Test Task from M365 Unified Skill', {
      priority: 5,
      description: 'This is a test task created by the M365 Unified skill',
    });
    console.log(`   ✅ Created task: ${testTask.title}`);
    console.log(`   ID: ${testTask.id}\n`);

    // Cleanup: Delete test task
    console.log('🧹 Cleaning up test task...');
    await client.planner.deleteTask(testTask.id);
    console.log('   ✅ Cleanup complete\n');
    */

    console.log('✅ Planner operations test complete!\n');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    if (error.response?.status === 403) {
      console.error('\n🚫 Permission error - check these API permissions:');
      console.error('   - Tasks.ReadWrite');
      console.error('   - Group.Read.All');
      console.error('   - Admin consent granted?');
    } else if (error.response?.status === 404) {
      console.error('\n📍 Not found - check Group ID:');
      console.error('   Group must have Planner enabled');
      console.error('   Verify Group ID is correct');
    }
    process.exit(1);
  }
}

testPlanner();
