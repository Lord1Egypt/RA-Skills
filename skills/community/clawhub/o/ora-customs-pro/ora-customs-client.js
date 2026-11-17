/**
 * Ora海关数据分析专家 - API Client
 *
 * Usage:
 *   node ora-customs-client.js --api=queryHsCodeProductSkill --dataarea=2 --importercountrytag=us --hs_code_product=家具 ...
 *   node ora-customs-client.js --api=queryImporterSkill --dataarea=1 --importer=APPLE+INC --importercountrytag=us
 *   node ora-customs-client.js --api=TradeIntelligenceAnalysis --dataType=1 --importer=APPLE+INC
 *   node ora-customs-client.js --api=queryShippingInfo --Product_Desc=furniture
 *
 * API Key 读取顺序：
 *   1. 环境变量 ORA_API_KEY
 *   2. 上级目录技能共享的 OraAgent.key
 *   3. 空字符串
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// --- Parse CLI args ---
const args = {};
let apiPath = '';
process.argv.slice(2).forEach(arg => {
  const m = arg.match(/^--([^=]+)=?(.*)$/);
  if (m) {
    if (m[1] === 'api') {
      apiPath = m[2];
    } else {
      args[m[1]] = m[2];
    }
  }
});

if (!apiPath) {
  console.error(JSON.stringify({ error: 'Missing --api parameter. Example: --api=queryHsCodeProductSkill' }));
  process.exit(1);
}

// --- Resolve API Key ---
// Try env var first, then look for OraAgent.key in parent skill dirs
let ORA_API_KEY = process.env.ORA_API_KEY || '';

if (!ORA_API_KEY) {
  const searchPaths = [
    path.join(__dirname, '..', 'OraAgent.key'),
    path.join(process.env.USERPROFILE || '', '.openclaw', 'workspace', 'skills', 'OraAgent.key'),
  ];
  for (const fp of searchPaths) {
    try {
      if (fs.existsSync(fp)) {
        ORA_API_KEY = fs.readFileSync(fp, 'utf8').trim();
        break;
      }
    } catch {}
  }
}

// --- Build POST body ---
const postParams = new URLSearchParams();
for (const [key, val] of Object.entries(args)) {
  postParams.append(key, val);
}
const postData = postParams.toString();

// --- Send request ---
const options = {
  hostname: 'h.smtso.com',
  path: '/skill/botcustoms/' + apiPath,
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Content-Length': Buffer.byteLength(postData),
    ...(ORA_API_KEY ? { 'X-API-Key': ORA_API_KEY } : {}),
  },
};

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
