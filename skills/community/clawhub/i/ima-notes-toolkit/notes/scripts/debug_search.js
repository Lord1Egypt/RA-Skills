#!/usr/bin/env node
const https = require('https');
const fs = require('fs');
const path = require('path');

let CLIENT_ID = process.env.IMA_OPENAPI_CLIENTID;

// 尝试从配置文件读取
if (!CLIENT_ID) {
  const configDir = path.join(process.env.USERPROFILE || process.env.HOME, '.config', 'ima');
  try { CLIENT_ID = fs.readFileSync(path.join(configDir, 'client_id'), 'utf8').trim(); } catch (e) {}
}
if (!CLIENT_ID) {
  try { 
    const skillEnv = path.join(process.env.USERPROFILE, '.workbuddy', 'skills', 'ima笔记', 'notes', '.env');
    const envContent = fs.readFileSync(skillEnv, 'utf8');
    const match = envContent.match(/IMA_CLIENT_ID\s*=\s*(.+)/);
    if (match) CLIENT_ID = match[1].trim();
  } catch (e) {}
}

const postData = JSON.stringify({
  search_type: 0,
  query_info: { title: '商事调解' },
  start: 0,
  end: 20
});

const options = {
  hostname: 'ima.qq.com',
  path: '/openapi/note/v1/search_note_book',
  method: 'POST',
  headers: {
    'ima-openapi-clientid': CLIENT_ID,
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const json = JSON.parse(data);
    console.log('Full response:');
    console.log(JSON.stringify(json, null, 2));
  });
});

req.on('error', console.error);
req.write(postData);
req.end();
