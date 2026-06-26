const https = require('https');
const config = require('./config');

/**
 * OTA Client
 * Handles communication with various OTA APIs.
 */
class OTAClient {
  constructor(platformKey) {
    this.platformKey = platformKey;
    this.platformConfig = config.get('platforms')[platformKey];
    
    if (!this.platformConfig || !this.platformConfig.apiKey) {
      console.warn(`[${platformKey}] Warning: No API configuration found. Client will run in MOCK mode.`);
    }
  }

  /**
   * Internal generic request handler
   */
  async _request(method, path, data) {
    if (!this.platformConfig || !this.platformConfig.apiKey) {
      console.log(`[MOCK][${this.platformKey}] ${method} ${path}`, data || '');
      return { status: 'mock_success' };
    }

    // Example of real network behavior scaffolding
    return new Promise((resolve, reject) => {
      const options = {
        hostname: new URL(this.platformConfig.endpoint).hostname,
        path: path,
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.platformConfig.apiKey}`
        }
      };

      const req = https.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => resolve(JSON.parse(body)));
      });

      req.on('error', (e) => reject(e));
      if (data) req.write(JSON.stringify(data));
      req.end();
    });
  }

  async updatePrice(roomTypeId, date, price) {
    return this._request('POST', '/update-price', { roomTypeId, date, price });
  }

  async updateInventory(roomTypeId, date, count) {
    return this._request('POST', '/update-inventory', { roomTypeId, date, count });
  }

  async setRoomStatus(roomTypeId, date, isOpen) {
    return this._request('POST', '/set-status', { roomTypeId, date, isOpen });
  }

  async fetchNewOrders() {
    if (!this.platformConfig || !this.platformConfig.apiKey) {
      return [{ id: `MOCK_ORD_${Date.now()}`, guest: 'Sample Guest', total: 0 }];
    }
    return this._request('GET', '/orders');
  }
}

module.exports = OTAClient;
