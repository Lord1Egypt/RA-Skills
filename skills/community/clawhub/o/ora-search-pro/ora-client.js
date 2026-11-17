/**
 * Ora外贸客户开发专家 - API Client
 * 
 * Usage:
 *   node ora-client.js --product=furniture --country=us --page=1 --limit=20
 *   node ora-client.js --company="ABC Co" --country=de --page=1 --limit=20
 *
 * API Key 读取顺序：
 *   1. 环境变量 ORA_API_KEY
 *   2. 同目录下的 OraAgent.key 文件
 *   3. 空字符串（接口可能返回未授权）
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const querystring = require('querystring');

// --- Parse CLI args ---
const args = {};
process.argv.slice(2).forEach(arg => {
  const m = arg.match(/^--([^=]+)=?(.*)$/);
  if (m) args[m[1]] = m[2];
});

// --- Resolve API Key ---
const keyFile = path.join(__dirname, 'OraAgent.key');
const ORA_API_KEY = process.env.ORA_API_KEY
  || (fs.existsSync(keyFile) ? fs.readFileSync(keyFile, 'utf8').trim() : '');

// --- Build request ---
const postData = querystring.stringify({
  CompanyName: args.company || '',
  ProductName: args.product || '',
  CountryTag: args.country || '',
  page: parseInt(args.page) || 1,
  limit: parseInt(args.limit) || 20,
});

const options = {
  hostname: 'h.smtso.com',
  path: '/skill/domaininfo/queryYellowPage',
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': Buffer.byteLength(postData),
    ...(ORA_API_KEY ? { 'X-API-Key': ORA_API_KEY } : {}),
  },
};

// --- Send request ---
const req = https.request(options, (res) => {
  let body = '';
  res.on('data', (chunk) => (body += chunk));
  res.on('end', () => {
    try {
      const parsed = JSON.parse(body);
      console.log(JSON.stringify(parsed, null, 2));
    } catch {
      console.log(body);
    }
  });
});

req.on('error', (err) => {
  console.error(JSON.stringify({ error: err.message }));
  process.exit(1);
});

req.write(postData);
req.end();
