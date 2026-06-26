const OTAClient = require('./ota_client');
const config = require('./config');

class OrderSyncService {
  constructor() {
    this.clients = Object.keys(config.get('platforms')).map(key => new OTAClient(key));
    this.internalPms = config.get('internalPms');
  }

  async syncOrders() {
    console.log(`[${new Date().toISOString()}] Starting order sync...`);
    
    for (const client of this.clients) {
      try {
        const orders = await client.fetchNewOrders();
        for (const order of orders) {
          await this.pushToInternalSystem(order, client.platformKey);
        }
      } catch (err) {
        console.error(`Error fetching orders from ${client.platformKey}:`, err.message);
      }
    }
  }

  async pushToInternalSystem(order, platformKey) {
    if (!this.internalPms.apiUrl) {
      console.log(`[MOCK][Sync] Pushing order ${order.id} from ${platformKey} to internal system...`);
      return { success: true };
    }

    console.log(`[Sync] Pushing order ${order.id} from ${platformKey} to ${this.internalPms.apiUrl}...`);
    // Real implementation would use fetch/https to push to internalPms.apiUrl
    return { success: true };
  }

  startAutoSync(intervalMs = 60000) {
    console.log(`Order sync service started (Interval: ${intervalMs}ms)`);
    setInterval(() => this.syncOrders(), intervalMs);
    this.syncOrders();
  }
}

// Example usage
if (require.main === module) {
  const service = new OrderSyncService();
  service.startAutoSync(300000); // Sync every 5 mins
}

module.exports = OrderSyncService;
