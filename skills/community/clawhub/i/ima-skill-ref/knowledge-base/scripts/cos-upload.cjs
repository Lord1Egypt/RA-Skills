#!/usr/bin/env node
'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const https = require('node:https');

const REQUIRED = ['file','bucket','region','cos-key'];

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 2) {
    const k = argv[i].replace(/^--/, '');
    const v = argv[i + 1];
    if (!v || v.startsWith('--')) { console.error(`Missing value for --${k}`); process.exit(1); }
    args[k] = v;
  }
  return args;
}

function loadCredentials(args) {
  // 优先从凭证文件加载
  if (args['cred-file']) {
    try {
      const credData = JSON.parse(fs.readFileSync(args['cred-file'], 'utf8'));
      // 使用后删除临时凭证文件
      try { fs.unlinkSync(args['cred-file']); } catch (e) { /* 忽略删除失败 */ }
      return {
        'secret-id': credData.secret_id,
        'secret-key': credData.secret_key,
        token: credData.token
      };
    } catch (e) {
      console.error(`警告: 无法读取凭证文件: ${e.message}`);
    }
  }
  
  // 回退到命令行参数
  return {
    'secret-id': args['secret-id'],
    'secret-key': args['secret-key'],
    token: args.token
  };
}

function hmacSha1(key, data) {
  return crypto.createHmac('sha1', key).update(data).digest('hex');
}

function sha1(data) {
  return crypto.createHash('sha1').update(data).digest('hex');
}

function buildAuth({ secretId, secretKey, method, pathname, headers, startTime, expiredTime }) {
  const keyTime = `${startTime};${expiredTime}`;
  const signKey = hmacSha1(secretKey, keyTime);
  const headerKeys = Object.keys(headers).sort();
  const httpHeaders = headerKeys.map(k => `${k.toLowerCase()}=${encodeURIComponent(headers[k])}`).join('&');
  const httpString = `${method.toLowerCase()}\n${pathname}\n\n${httpHeaders}\n`;
  const stringToSign = `sha1\n${keyTime}\n${sha1(httpString)}\n`;
  const signature = hmacSha1(signKey, stringToSign);
  const headerList = headerKeys.map(k => k.toLowerCase()).join(';');
  return `q-sign-algorithm=sha1&q-ak=${secretId}&q-sign-time=${keyTime}&q-key-time=${keyTime}&q-header-list=${headerList}&q-url-param-list=&q-signature=${signature}`;
}

function upload(args) {
  const { file, 'secret-id': secretId, 'secret-key': secretKey, token, bucket, region, 'cos-key': cosKey } = args;
  const startTime = args['start-time'] || String(Math.floor(Date.now() / 1000));
  const expiredTime = args['expired-time'] || String(Math.floor(Date.now() / 1000) + 3600);
  const content = fs.readFileSync(file);
  const hostname = `${bucket}.cos.${region}.myqcloud.com`;
  const pathname = `/${cosKey}`;
  const contentType = args['content-type'] || 'application/octet-stream';

  const signHeaders = { 'content-length': String(content.length), host: hostname };
  const authorization = buildAuth({ secretId, secretKey, method: 'PUT', pathname, headers: signHeaders, startTime, expiredTime });

  const options = {
    hostname, port: 443, path: pathname, method: 'PUT',
    headers: { 'Content-Type': contentType, 'Content-Length': content.length, Authorization: authorization, 'x-cos-security-token': token }
  };

  const req = https.request(options, res => {
    let body = '';
    res.on('data', c => body += c);
    res.on('end', () => {
      if (res.statusCode >= 200 && res.statusCode < 300) { console.log(`Upload successful (HTTP ${res.statusCode})`); process.exit(0); }
      else { console.error(`COS upload failed (HTTP ${res.statusCode}): ${body}`); process.exit(1); }
    });
  });

  req.on('error', e => { console.error(`COS upload error: ${e.message}`); process.exit(1); });
  req.write(content);
  req.end();
}

const args = parseArgs(process.argv);
const missing = REQUIRED.filter(k => !args[k]);
if (missing.length) {
  console.error(`Missing required arguments: ${missing.map(k => `--${k}`).join(', ')}`);
  process.exit(1);
}
if (!fs.existsSync(args.file)) {
  console.error(`File not found: ${args.file}`);
  process.exit(1);
}

// 加载凭证（优先从文件，其次从命令行参数）
const credentials = loadCredentials(args);
if (!credentials['secret-id'] || !credentials['secret-key'] || !credentials.token) {
  console.error('Missing required credentials. Provide either --cred-file or --secret-id/--secret-key/--token');
  process.exit(1);
}

// 合并凭证到args
const uploadArgs = { ...args, ...credentials };
upload(uploadArgs);
