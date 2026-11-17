/**
 * fetcher.js — Fetch and extract article content from a URL
 * Falls back through multiple strategies for resilient extraction.
 */
const https = require('https');
const http  = require('http');

function fetchUrl(targetUrl) {
  return new Promise((resolve, reject) => {
    let redirected = false;
    const lib = targetUrl.startsWith('https') ? https : http;
    const req = lib.get(targetUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
      }
    }, res => {
      // Follow up to 3 redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        if (redirected) { reject(new Error('Too many redirects')); return; }
        redirected = true;
        const next = new URL(res.headers.location, targetUrl).toString();
        fetchUrl(next).then(resolve).catch(reject);
        return;
      }
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    });
    req.on('error', reject);
    req.setTimeout(20000, () => { req.destroy(); reject(new Error('Request timeout')); });
  });
}

function htmlToText(html) {
  if (!html || html.length < 100) return '';
  return html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<noscript[^>]*>[\s\S]*?<\/noscript>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<([a-z][a-z0-9]*)[^>]*(?:\/>|[^>]*>)/gi, ' $1 ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ')
    .replace(/https?:\/\/\S+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function extractTitle(text) {
  if (!text) return 'Unknown';
  const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 20 && l.length < 200);
  return lines[0] ? lines[0].slice(0, 120) : 'Unknown';
}

module.exports = { fetchUrl, htmlToText, extractTitle };
