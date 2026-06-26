#!/usr/bin/env node
/**
 * Auto-Renew Webhook Subscriptions
 * 
 * Wird täglich via Cron ausgeführt und erneuert Webhooks
 * die in den nächsten 24 Stunden ablaufen würden.
 */

import dotenv from 'dotenv';
import { getAccessToken } from '../src/auth/graph-client.js';
import * as webhooks from '../src/webhooks/subscriptions.js';

dotenv.config();

const RENEW_THRESHOLD_HOURS = 24; // Renew wenn < 24 Stunden verbleiben

async function autoRenewWebhooks() {
  console.log(`⏰ Auto-Renew Webhooks - ${new Date().toISOString()}`);
  console.log('='.repeat(50));

  try {
    const token = await getAccessToken({
      tenantId: process.env.M365_TENANT_ID,
      clientId: process.env.M365_CLIENT_ID,
      clientSecret: process.env.M365_CLIENT_SECRET,
    });

    const subscriptions = await webhooks.listSubscriptions(token);

    if (subscriptions.length === 0) {
      console.log('ℹ️  Keine aktiven Webhook-Subscriptions');
      return;
    }

    const now = new Date();
    let renewed = 0;
    let expired = 0;

    for (const sub of subscriptions) {
      const expires = new Date(sub.expirationDateTime);
      const hoursLeft = (expires - now) / (1000 * 60 * 60);

      console.log(`\n📌 ${sub.id}`);
      console.log(`   Resource: ${sub.resource}`);
      console.log(`   Expires: ${sub.expirationDateTime}`);
      console.log(`   Hours left: ${hoursLeft.toFixed(1)}`);

      if (hoursLeft <= 0) {
        console.log('   ❌ EXPIRED - Creating new subscription needed');
        expired++;
        // Hier könnte man automatisch neue Subscription erstellen
        continue;
      }

      if (hoursLeft <= RENEW_THRESHOLD_HOURS) {
        console.log(`   ⚠️  RENEWING (expires in < ${RENEW_THRESHOLD_HOURS}h)`);
        
        try {
          const newExpiration = webhooks.calculateExpirationDate(3); // 3 Tage verlängern
          const updated = await webhooks.renewSubscription(token, sub.id, newExpiration);
          
          console.log(`   ✅ Renewed until: ${updated.expirationDateTime}`);
          renewed++;
        } catch (error) {
          console.error(`   ❌ Renewal failed: ${error.message}`);
          // Fallback: Neue Subscription erstellen wenn Renewal fehlschlägt
        }
      } else {
        console.log('   ✅ OK - No action needed');
      }
    }

    console.log('\n' + '='.repeat(50));
    console.log(`Summary: ${renewed} renewed, ${expired} expired`);

  } catch (error) {
    console.error('❌ Auto-renew failed:');
    console.error(`   ${error.message}`);
    process.exit(1);
  }
}

autoRenewWebhooks().catch(console.error);
