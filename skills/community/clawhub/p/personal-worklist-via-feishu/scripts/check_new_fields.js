const path = require('path');
const fs = require('fs');
const https = require('https');

// Find openclaw.json
let dir = __dirname;
for (let i = 0; i < 4; i++) { dir = path.dirname(dir); }
const openclawPath = path.join(dir, 'openclaw.json');
const openclawConfig = JSON.parse(fs.readFileSync(openclawPath, 'utf8'));
const feishu = openclawConfig?.channels?.feishu;

const data = JSON.stringify({ app_id: feishu.appId, app_secret: feishu.appSecret });
const options = {
  hostname: 'open.feishu.cn',
  path: '/open-apis/auth/v3/tenant_access_token/internal',
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
};
const req = https.request(options, (res) => {
  let body = '';
  res.on('data', c => body += c);
  res.on('end', () => {
    const token = JSON.parse(body).tenant_access_token;
    console.log('Token: OK');
    
    // Get fields
    const getOpts = {
      hostname: 'open.feishu.cn',
      path: '/open-apis/bitable/v1/apps/V97jbff3fazN8HszN40c6QESndd/tables/tblR4Zj5iYomhLsq/fields',
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + token }
    };
    const getReq = https.request(getOpts, (res2) => {
      let b2 = '';
      res2.on('data', c => b2 += c);
      res2.on('end', () => {
        const fields = JSON.parse(b2);
        if (fields.code === 0) {
          console.log('\nFields in new bitable:');
          fields.data.items.forEach(f => {
            console.log(`  ${f.field_name}: type=${f.type}, ui_type=${f.ui_type}`);
          });
        } else {
          console.log('Error getting fields:', b2);
        }
      });
    });
    getReq.end();
  });
});
req.write(data);
req.end();
