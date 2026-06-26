/**
 * Config Loader
 * Safeguards credentials by prioritizing Environment Variables over local JSON files.
 */

const fs = require('fs');
const path = require('path');

class Config {
  constructor() {
    this.values = {};
    this.load();
  }

  load() {
    // 1. Try to load from environment variables (Highest priority)
    this.values = {
      platforms: {
        ctrip: {
          apiKey: process.env.OTA_CTRIP_API_KEY,
          secret: process.env.OTA_CTRIP_SECRET,
          endpoint: process.env.OTA_CTRIP_ENDPOINT || 'https://api.ctrip.com/hotel/v1'
        },
        meituan: {
          apiKey: process.env.OTA_MEITUAN_API_KEY,
          secret: process.env.OTA_MEITUAN_SECRET,
          endpoint: process.env.OTA_MEITUAN_ENDPOINT || 'https://api.meituan.com/hotel/v1'
        }
      },
      internalPms: {
        apiUrl: process.env.INTERNAL_PMS_URL,
        token: process.env.INTERNAL_PMS_TOKEN
      }
    };

    // 2. Try to load from a local config file if not fully provided by ENV
    const configPath = process.env.HOTEL_MANAGER_CONFIG_PATH || path.join(__dirname, '../resources/ota_config.json');
    if (fs.existsSync(configPath)) {
      try {
        const fileContent = fs.readFileSync(configPath, 'utf8');
        const fileConfig = JSON.parse(fileContent);
        this.merge(fileConfig);
      } catch (err) {
        console.warn(`Warning: Could not parse config file at ${configPath}: ${err.message}`);
      }
    }
  }

  merge(fileConfig) {
    // Deep merge logic simplified for this skill
    if (fileConfig.platforms) {
      fileConfig.platforms.forEach(p => {
        const key = this.mapKey(p.name);
        if (key && this.values.platforms[key]) {
          this.values.platforms[key].apiKey = this.values.platforms[key].apiKey || p.api_key;
          this.values.platforms[key].secret = this.values.platforms[key].secret || p.secret;
          this.values.platforms[key].endpoint = this.values.platforms[key].endpoint || p.api_endpoint;
        }
      });
    }
    if (fileConfig.internal_pms) {
      this.values.internalPms.apiUrl = this.values.internalPms.apiUrl || fileConfig.internal_pms.api_url;
      this.values.internalPms.token = this.values.internalPms.token || fileConfig.internal_pms.token;
    }
  }

  mapKey(name) {
    if (name.includes('携程')) return 'ctrip';
    if (name.includes('美团')) return 'meituan';
    return null;
  }

  get(key) {
    return this.values[key];
  }
}

module.exports = new Config();
