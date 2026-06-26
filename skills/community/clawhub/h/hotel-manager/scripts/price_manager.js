const OTAClient = require('./ota_client');
const config = require('./config');

class PriceManager {
  constructor() {
    this.clients = Object.keys(config.get('platforms')).map(key => new OTAClient(key));
  }

  /**
   * Update prices across all platforms with a base price.
   */
  async updateUnifiedPrice(roomTypeId, date, basePrice) {
    console.log(`--- Starting Unified Price Update for ${roomTypeId} on ${date} (Base: ${basePrice}) ---`);
    
    const results = await Promise.all(this.clients.map(async client => {
      // Example logic: Different platforms might have different markups
      let platformPrice = basePrice;
      if (client.platformKey === 'ctrip') platformPrice += 10;
      if (client.platformKey === 'meituan') platformPrice -= 5;
      
      return await client.updatePrice(roomTypeId, date, platformPrice);
    }));

    console.log('--- Unified Update Finished ---');
    return results;
  }
}

// Example usage
if (require.main === module) {
  const manager = new PriceManager();
  manager.updateUnifiedPrice('RM_001', '2024-05-01', 500);
}

module.exports = PriceManager;
