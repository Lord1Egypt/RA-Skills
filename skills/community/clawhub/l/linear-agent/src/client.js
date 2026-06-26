/**
 * src/client.js
 * Zero-dependency GraphQL client for the Linear API.
 * Uses Node's built-in https module — no npm install required.
 */

'use strict';

const https = require('https');

const LINEAR_ENDPOINT = 'https://api.linear.app/graphql';

class LinearClient {
  /**
   * @param {string} apiKey - Linear personal API key (lin_api_...)
   */
  constructor(apiKey) {
    if (!apiKey) {
      throw new Error(
        'LINEAR_API_KEY is required. ' +
        'Set it as an environment variable or pass it explicitly.\n' +
        'Get yours at: https://linear.app/settings/api'
      );
    }
    this.apiKey = apiKey;
  }

  /**
   * Execute a GraphQL operation against the Linear API.
   *
   * @param {string} query      - GraphQL query or mutation string
   * @param {object} variables  - Variables map
   * @returns {Promise<object>} - The `data` field from the response
   * @throws {Error}            - On network failure or GraphQL errors
   */
  async request(query, variables = {}) {
    const body = JSON.stringify({ query, variables });

    return new Promise((resolve, reject) => {
      const options = {
        hostname: 'api.linear.app',
        path: '/graphql',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': this.apiKey,
          'Content-Length': Buffer.byteLength(body),
          'User-Agent': 'linear-agent-openclaw/1.0.0',
        },
      };

      const req = https.request(options, (res) => {
        let raw = '';
        res.on('data', (chunk) => { raw += chunk; });
        res.on('end', () => {
          // Handle non-200 HTTP status codes
          if (res.statusCode === 401 || res.statusCode === 403) {
            return reject(new Error(
              `Authentication failed (HTTP ${res.statusCode}). ` +
              'Check that your LINEAR_API_KEY is valid and has not expired.'
            ));
          }

          let parsed;
          try {
            parsed = JSON.parse(raw);
          } catch (e) {
            return reject(new Error(
              `Failed to parse Linear API response: ${e.message}\nRaw: ${raw.slice(0, 200)}`
            ));
          }

          // Surface GraphQL-level errors (not HTTP errors)
          if (parsed.errors && parsed.errors.length > 0) {
            const msgs = parsed.errors.map((e) => e.message).join('; ');
            return reject(new Error(`Linear GraphQL error: ${msgs}`));
          }

          resolve(parsed.data);
        });
      });

      req.on('error', (err) => {
        reject(new Error(`Network error reaching Linear API: ${err.message}`));
      });

      req.write(body);
      req.end();
    });
  }
}

module.exports = { LinearClient };
