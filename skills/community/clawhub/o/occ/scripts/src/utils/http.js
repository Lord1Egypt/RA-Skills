const http = require('http');

const DEFAULT_PORT = 4096;
const DEFAULT_HOST = '127.0.0.1';

function getBaseUrl(host = DEFAULT_HOST, port = DEFAULT_PORT) {
  return `http://${host}:${port}`;
}

function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const reqOptions = { ...options };
    if (options.body && !options.headers?.['Content-Length']) {
      reqOptions.headers = {
        ...reqOptions.headers,
        'Content-Length': Buffer.byteLength(options.body)
      };
    }
    
    const req = http.request(url, reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    if (options.body) {
      req.write(options.body);
    }
    req.end();
  });
}

module.exports = {
  httpRequest,
  getBaseUrl,
  DEFAULT_PORT,
  DEFAULT_HOST
};