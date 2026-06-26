/**
 * APITester — Agent-Driven API Testing
 * @author @TheShadowRose
 * @license MIT
 */
const https = require('https');
const http = require('http');
const fs = require('fs');

class APITester {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || '';
    this.headers = options.headers || {};
    this.results = [];
    this.variables = {};
  }

  async runTests(tests) {
    this.results = [];
    for (const test of tests) {
      const result = await this._runOne(test);
      this.results.push(result);
      // Store variables from response
      if (test.store && result.body) {
        for (const [key, jsonPath] of Object.entries(test.store)) {
          this.variables[key] = this._extract(result.body, jsonPath);
        }
      }
    }
    const passed = this.results.filter(r => r.passed).length;
    const total = this.results.length;
    return {
      total, passed, failed: total - passed,
      passRate: total > 0 ? Math.round(passed / total * 100) + '%' : '0%',
      avgResponseTime: total > 0 ? Math.round(this.results.reduce((s, r) => s + r.responseTime, 0) / total) : 0,
      results: this.results
    };
  }

  async _runOne(test) {
    const url = this._interpolate((this.baseUrl + (test.url || '')));
    const method = (test.method || 'GET').toUpperCase();
    const start = Date.now();
    
    try {
      const res = await this._request(url, method, test.body ? JSON.stringify(this._interpolateObj(test.body)) : null, { ...this.headers, ...test.headers });
      const responseTime = Date.now() - start;
      let passed = true;
      const checks = [];

      if (test.expect) {
        if (test.expect.status && res.statusCode !== test.expect.status) {
          passed = false;
          checks.push(`Expected status ${test.expect.status}, got ${res.statusCode}`);
        }
        if (test.expect.body_contains && !res.body.includes(test.expect.body_contains)) {
          passed = false;
          checks.push(`Body missing: ${test.expect.body_contains}`);
        }
        if (test.expect.response_time) {
          const max = parseInt(test.expect.response_time);
          if (responseTime > max) { passed = false; checks.push(`Slow: ${responseTime}ms > ${max}ms`); }
        }
      }

      return { name: test.name, passed, status: res.statusCode, responseTime, checks, body: res.body };
    } catch (err) {
      return { name: test.name, passed: false, error: err.message, responseTime: Date.now() - start, checks: [err.message] };
    }
  }

  _request(url, method, body, headers) {
    const client = url.startsWith('https') ? https : http;
    const parsed = new URL(url);
    return new Promise((resolve, reject) => {
      const req = client.request({
        hostname: parsed.hostname, port: parsed.port, path: parsed.pathname + parsed.search,
        method, headers: { 'Content-Type': 'application/json', ...headers }, timeout: 10000
      }, res => {
        let data = '';
        res.on('data', c => data += c);
        res.on('end', () => resolve({ statusCode: res.statusCode, headers: res.headers, body: data }));
      });
      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
      if (body) req.write(body);
      req.end();
    });
  }

  _interpolate(str) {
    return str.replace(/\{\{([^}]+)\}\}/g, (_, key) => {
      const val = this.variables[key.trim()];
      return val != null ? String(val) : '';
    });
  }

  _interpolateObj(obj) {
    // Interpolate values safely by walking the object, not string-replacing inside JSON
    const walk = (o) => {
      if (typeof o === 'string') return this._interpolate(o);
      if (Array.isArray(o)) return o.map(walk);
      if (o && typeof o === 'object') {
        const out = {};
        for (const [k, v] of Object.entries(o)) out[k] = walk(v);
        return out;
      }
      return o;
    };
    return walk(obj);
  }

  _extract(body, jsonPath) {
    try { const obj = JSON.parse(body); return jsonPath.split('.').reduce((o, k) => o[k], obj); }
    catch { return null; }
  }

  format() {
    const lines = ['API Test Results\n'];
    for (const r of this.results) {
      const icon = r.passed ? '✅' : '❌';
      lines.push(`${icon} ${r.name}  ${r.status || 'ERR'}  ${r.responseTime}ms`);
      for (const c of (r.checks || [])) lines.push(`   ⚠️ ${c}`);
    }
    const passed = this.results.filter(r => r.passed).length;
    lines.push(`\nPass: ${passed}/${this.results.length}`);
    return lines.join('\n');
  }
}

module.exports = { APITester };
