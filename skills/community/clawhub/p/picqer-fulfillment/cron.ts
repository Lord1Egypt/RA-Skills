import { processDashboardData } from './tools/data-processor.js';

// Auto-refresh every 5 minutes
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes in ms

async function syncData() {
  try {
    console.log('🔄 Syncing Picqer data...');
    await processDashboardData();
    console.log('✅ Picqer data synced at', new Date().toISOString());
  } catch (e) {
    console.error('❌ Sync failed:', e);
  }
}

// Initial sync
syncData();

// Schedule recurring sync
setInterval(syncData, REFRESH_INTERVAL);

console.log('📊 FutureFulfillment Dashboard auto-refresh started (5 min intervals)');
