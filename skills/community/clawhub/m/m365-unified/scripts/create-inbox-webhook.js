#!/usr/bin/env node
/**
 * Quick Script: Create Inbox Webhook Subscription
 * Fixed path for .env loading
 */

import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.join(__dirname, '..');

// Load .env from skill directory
dotenv.config({ path: path.join(skillDir, '.env') });

console.log('🔔 Creating Inbox Webhook Subscription...\n');
console.log('Working Directory:', skillDir);
console.log('WEBHOOK_URL:', process.env.M365_WEBHOOK_URL || 'NOT SET');
console.log('MAILBOX:', process.env.M365_MAILBOX || 'NOT SET');
console.log('');

if (!process.env.M365_WEBHOOK_URL) {
  console.error('❌ M365_WEBHOOK_URL not configured!');
  process.exit(1);
}

// Change to skill directory and run the manage-webhooks script
try {
  const result = execSync(
    `node scripts/manage-webhooks.js create --resource=mail_inbox --type=created --days=3`,
    {
      cwd: skillDir,
      encoding: 'utf8',
      stdio: 'inherit',
    }
  );
} catch (error) {
  console.error('Failed to create webhook');
  process.exit(1);
}
