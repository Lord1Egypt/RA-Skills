#!/usr/bin/env node
/**
 * ZhenRent API Client
 * Handles authentication and communication with ZhenRent platform
 */

const crypto = require('crypto');
const https = require('https');
const http = require('http');

class ZhenRentAPIClient {
  constructor() {
    this.apiKey = process.env.ZHENRENT_API_KEY;
    this.apiSecret = process.env.ZHENRENT_API_SECRET;
    this.baseUrl = process.env.ZHENRENT_BASE_URL || 'https://www.zhenrent.com/api/v1';

    if (!this.apiKey || !this.apiSecret) {
      throw new Error(
        'Missing credentials. Please set ZHENRENT_API_KEY and ZHENRENT_API_SECRET environment variables.\n' +
        'Get your credentials at: https://www.zhenrent.com/api/keys'
      );
    }

    // Validate base URL to prevent SSRF attacks
    this.validateBaseUrl();
  }

  /**
   * Validate base URL to prevent SSRF attacks
   * @private
   */
  validateBaseUrl() {
    let url;
    try {
      url = new URL(this.baseUrl);
    } catch (e) {
      throw new Error(`Invalid ZHENRENT_BASE_URL: ${this.baseUrl}`);
    }

    // 1. Enforce HTTPS only
    if (url.protocol !== 'https:') {
      throw new Error(
        `Security Error: ZHENRENT_BASE_URL must use https:// protocol (got: ${url.protocol})\n` +
        'This requirement protects your API credentials from being transmitted insecurely.'
      );
    }

    // 2. Whitelist allowed hostnames
    const allowedHosts = [
      'www.zhenrent.com',
      'api.zhenrent.com',
      'zhenrent.com'
    ];

    if (!allowedHosts.includes(url.hostname)) {
      throw new Error(
        `Security Error: ZHENRENT_BASE_URL hostname must be one of: ${allowedHosts.join(', ')}\n` +
        `Got: ${url.hostname}\n` +
        'This requirement prevents Server-Side Request Forgery (SSRF) attacks.'
      );
    }

    // 3. Block internal IP addresses (defense in depth)
    const hostname = url.hostname;

    // Check for localhost
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1') {
      throw new Error(
        'Security Error: ZHENRENT_BASE_URL cannot point to localhost.\n' +
        'This prevents accessing internal services.'
      );
    }

    // Check for private IP ranges
    const privateIpPatterns = [
      /^127\./,                           // 127.0.0.0/8 (loopback)
      /^10\./,                            // 10.0.0.0/8 (private)
      /^172\.(1[6-9]|2[0-9]|3[01])\./,   // 172.16.0.0/12 (private)
      /^192\.168\./,                      // 192.168.0.0/16 (private)
      /^169\.254\./                       // 169.254.0.0/16 (link-local)
    ];

    for (const pattern of privateIpPatterns) {
      if (pattern.test(hostname)) {
        throw new Error(
          `Security Error: ZHENRENT_BASE_URL cannot point to internal IP addresses (got: ${hostname}).\n` +
          'This prevents accessing internal services.'
        );
      }
    }
  }

  /**
   * Generate HMAC-SHA256 signature for request authentication
   */
  generateSignature(method, path, timestamp, body) {
    const message = `${method}${path}${timestamp}${body}`;
    return crypto
      .createHmac('sha256', this.apiSecret)
      .update(message)
      .digest('hex');
  }

  /**
   * Make authenticated API request
   */
  async request(method, path, data = null) {
    const timestamp = Date.now().toString();
    const body = data ? JSON.stringify(data) : '';
    const signature = this.generateSignature(method, path, timestamp, body);

    const url = new URL(this.baseUrl + path);
    const isHttps = url.protocol === 'https:';
    const httpModule = isHttps ? https : http;

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
        'X-Timestamp': timestamp,
        'X-Signature': signature,
      },
    };

    if (body) {
      options.headers['Content-Length'] = Buffer.byteLength(body);
    }

    return new Promise((resolve, reject) => {
      const req = httpModule.request(options, (res) => {
        let responseData = '';

        res.on('data', (chunk) => {
          responseData += chunk;
        });

        res.on('end', () => {
          try {
            const parsed = JSON.parse(responseData);
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(parsed);
            } else {
              reject(new Error(`API Error (${res.statusCode}): ${parsed.error || responseData}`));
            }
          } catch (e) {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve({ data: responseData });
            } else {
              reject(new Error(`API Error (${res.statusCode}): ${responseData}`));
            }
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`Network error: ${error.message}`));
      });

      if (body) {
        req.write(body);
      }

      req.end();
    });
  }

  /**
   * Create a new task
   */
  async createTask(taskData) {
    return this.request('POST', '/tasks/', taskData);
  }

  /**
   * Get task status
   */
  async getTaskStatus(taskId) {
    return this.request('GET', `/tasks/${taskId}`);
  }

  /**
   * List available workers
   */
  async listWorkers(location = null, radius = 5000) {
    let path = '/workers/';
    if (location) {
      path += `?location=${location}&radius=${radius}`;
    }
    return this.request('GET', path);
  }

  /**
   * Cancel a task
   */
  async cancelTask(taskId) {
    return this.request('POST', `/tasks/${taskId}/cancel`);
  }
}

module.exports = ZhenRentAPIClient;
