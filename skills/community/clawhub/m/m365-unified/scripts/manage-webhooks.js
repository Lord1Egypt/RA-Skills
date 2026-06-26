#!/usr/bin/env node
/**
 * Webhook Subscription Management
 * 
 * Create, list, renew, and delete webhook subscriptions for Microsoft Graph.
 */

import dotenv from 'dotenv';
import axios from 'axios';
import { getAccessToken } from '../src/auth/graph-client.js';
import * as webhooks from '../src/webhooks/subscriptions.js';

dotenv.config();

// Parse command line arguments
const args = process.argv.slice(2);
const command = args[0];
const options = {};

args.slice(1).forEach(arg => {
  if (arg.startsWith('--')) {
    const [key, value] = arg.slice(2).split('=');
    options[key] = value || true;
  }
});

async function createWebhook() {
  console.log('🔔 Creating Webhook Subscription...\n');

  // Validate required config
  if (!process.env.M365_WEBHOOK_URL) {
    console.error('❌ M365_WEBHOOK_URL not configured in .env');
    process.exit(1);
  }

  const resource = options.resource || 'mail';
  const resourcePath = getResourcePath(resource);

  console.log(`Resource: ${resourcePath}`);
  console.log(`Webhook URL: ${process.env.M365_WEBHOOK_URL}`);
  console.log(`Change Types: ${options.type || 'created'}`);
  console.log(`Duration: ${options.days || 3} days\n`);

  try {
    const token = await getAccessToken({
      tenantId: process.env.M365_TENANT_ID,
      clientId: process.env.M365_CLIENT_ID,
      clientSecret: process.env.M365_CLIENT_SECRET,
    });

    const expirationDateTime = webhooks.calculateExpirationDate(parseInt(options.days) || 3);

    const subscription = await webhooks.createSubscription(token, {
      resource: resourcePath,
      changeType: options.type || 'created,updated,deleted',
      notificationUrl: process.env.M365_WEBHOOK_URL,
      expirationDateTime,
      clientState: process.env.M365_WEBHOOK_SECRET || 'secret' + Date.now(),
    });

    console.log('✅ Webhook subscription created!');
    console.log(`   ID: ${subscription.id}`);
    console.log(`   Resource: ${subscription.resource}`);
    console.log(`   Expires: ${subscription.expirationDateTime}`);
    console.log(`\n⚠️  Important: Renew before expiration!`);
    console.log(`   Command: node scripts/manage-webhooks.js renew --id=${subscription.id} --days=3\n`);

  } catch (error) {
    console.error('❌ Failed to create webhook:');
    console.error(`   ${error.response?.data?.error?.message || error.message}`);
    
    if (error.response?.status === 400) {
      console.error('\n💡 Tips:');
      console.error('   - Webhook URL must be publicly accessible (HTTPS)');
      console.error('   - URL must respond to validation challenge within 120 seconds');
      console.error('   - Check Azure AD app permissions (User.Read minimum)');
    }
    
    process.exit(1);
  }
}

async function listWebhooks() {
  console.log('📋 Listing Webhook Subscriptions...\n');

  try {
    const token = await getAccessToken({
      tenantId: process.env.M365_TENANT_ID,
      clientId: process.env.M365_CLIENT_ID,
      clientSecret: process.env.M365_CLIENT_SECRET,
    });

    const subscriptions = await webhooks.listSubscriptions(token);

    if (subscriptions.length === 0) {
      console.log('ℹ️  No active webhook subscriptions\n');
      return;
    }

    console.log(`Found ${subscriptions.length} subscription(s):\n`);
    
    subscriptions.forEach(sub => {
      const expires = new Date(sub.expirationDateTime);
      const now = new Date();
      const daysLeft = Math.ceil((expires - now) / (1000 * 60 * 60 * 24));
      
      console.log(`📌 ${sub.id}`);
      console.log(`   Resource: ${sub.resource}`);
      console.log(`   Change Types: ${sub.changeType}`);
      console.log(`   Expires: ${sub.expirationDateTime} (${daysLeft} days left)`);
      console.log(`   Status: ${daysLeft <= 1 ? '⚠️  RENEW SOON' : '✅ Active'}\n`);
    });

  } catch (error) {
    console.error('❌ Failed to list webhooks:');
    console.error(`   ${error.message}`);
    process.exit(1);
  }
}

async function renewWebhook() {
  console.log('🔄 Renewing Webhook Subscription...\n');

  if (!options.id) {
    console.error('❌ Subscription ID required: --id=<subscription-id>');
    process.exit(1);
  }

  try {
    const token = await getAccessToken({
      tenantId: process.env.M365_TENANT_ID,
      clientId: process.env.M365_CLIENT_ID,
      clientSecret: process.env.M365_CLIENT_SECRET,
    });

    const expirationDateTime = webhooks.calculateExpirationDate(parseInt(options.days) || 3);

    const subscription = await webhooks.renewSubscription(token, options.id, expirationDateTime);

    console.log('✅ Webhook subscription renewed!');
    console.log(`   ID: ${subscription.id}`);
    console.log(`   New Expiration: ${subscription.expirationDateTime}\n`);

  } catch (error) {
    console.error('❌ Failed to renew webhook:');
    console.error(`   ${error.response?.data?.error?.message || error.message}`);
    process.exit(1);
  }
}

async function deleteWebhook() {
  console.log('🗑️  Deleting Webhook Subscription...\n');

  if (!options.id) {
    console.error('❌ Subscription ID required: --id=<subscription-id>');
    process.exit(1);
  }

  try {
    const token = await getAccessToken({
      tenantId: process.env.M365_TENANT_ID,
      clientId: process.env.M365_CLIENT_ID,
      clientSecret: process.env.M365_CLIENT_SECRET,
    });

    await webhooks.deleteSubscription(token, options.id);

    console.log('✅ Webhook subscription deleted\n');

  } catch (error) {
    console.error('❌ Failed to delete webhook:');
    console.error(`   ${error.message}`);
    process.exit(1);
  }
}

function getResourcePath(resource) {
  const mailbox = process.env.M365_MAILBOX || 'user@domain.com';
  
  const paths = {
    mail: `users/${mailbox}/messages`,
    mail_inbox: `users/${mailbox}/mailFolders/inbox/messages`,
    mail_sent: `users/${mailbox}/mailFolders/sentitems/messages`,
    sharepoint: `sites/${process.env.M365_SHAREPOINT_SITE_ID || '{site-id}'}/drive/root`,
    onedrive: 'me/drive/root',
    planner: `planner/plans/${options.planId || '{plan-id}'}/tasks`,
  };

  return paths[resource] || paths.mail;
}

function showHelp() {
  console.log(`
📡 Webhook Subscription Management

Usage:
  node scripts/manage-webhooks.js <command> [options]

Commands:
  create    Create new webhook subscription
  list      List all active subscriptions
  renew     Renew existing subscription
  delete    Delete subscription

Options:
  --resource=<type>     Resource to monitor (mail, mail_inbox, sharepoint, onedrive, planner)
  --type=<changes>      Change types (created,updated,deleted) - default: created
  --days=<number>       Subscription duration in days - default: 3
  --id=<subscription>   Subscription ID (for renew/delete)
  --planId=<id>         Planner Plan ID (for planner webhooks)

Examples:
  # Create webhook for new emails
  node scripts/manage-webhooks.js create --resource=mail --type=created

  # Create webhook for SharePoint file changes
  node scripts/manage-webhooks.js create --resource=sharepoint --type=created,updated

  # List all webhooks
  node scripts/manage-webhooks.js list

  # Renew webhook for 3 more days
  node scripts/manage-webhooks.js renew --id=abc123 --days=3

  # Delete webhook
  node scripts/manage-webhooks.js delete --id=abc123

Notes:
  - Webhooks expire after 3 days maximum - set up auto-renewal!
  - Your webhook URL must be publicly accessible (HTTPS)
  - Webhook endpoint must handle validation challenge on first creation
  - See docs/webhooks.md for complete setup guide
`);
}

// Main execution
async function main() {
  if (!command || command === 'help' || command === '--help') {
    showHelp();
    return;
  }

  switch (command) {
    case 'create':
      await createWebhook();
      break;
    case 'list':
      await listWebhooks();
      break;
    case 'renew':
      await renewWebhook();
      break;
    case 'delete':
      await deleteWebhook();
      break;
    default:
      console.error(`❌ Unknown command: ${command}`);
      showHelp();
      process.exit(1);
  }
}

main().catch(console.error);
