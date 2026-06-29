import { getAlertsMessage, getPathAlerts } from './index.js';

console.log('Testing NJ PATH Alerts plugin...\n');

// Test 1: Get raw alerts
console.log('1. Fetching raw alerts...');
const alerts = await getPathAlerts();
console.log(`Found ${alerts.length} active alerts\n`);

// Test 2: Get formatted message
console.log('2. Formatted message:');
console.log('---');
const message = await getAlertsMessage();
console.log(message);
console.log('---\n');

console.log('✅ Test complete!');
