#!/usr/bin/env node

const http = require('http');
const https = require('https');

/**
 * 客户端脚本：调用远程 API 进行新闻内容提取
 */

// 后端 API 地址（建议在实际使用时改为您的生产服务器地址）
const SERVER_URL = process.env.NEWS_EXTRACTOR_SERVER_URL || 'https://easyalpha.duckdns.org/api/v1/extract';
const API_KEY = process.env.EASYALPHA_API_KEY;

const urlToExtract = process.argv[2];

if (!urlToExtract) {
  console.error(JSON.stringify({ error: "请输入新闻 URL" }));
  process.exit(1);
}

if (!API_KEY) {
  console.error(JSON.stringify({ error: "缺失环境变量 EASYALPHA_API_KEY，请在配置中设置。" }));
  process.exit(1);
}

// 构造请求 URL
const targetUrl = new URL(SERVER_URL);
targetUrl.searchParams.append('url', urlToExtract);

const options = {
  headers: {
    'Authorization': API_KEY
  },
  rejectUnauthorized: false // 跳过 SSL 证书验证，解决 "unable to verify the first certificate" 错误
};

const client = targetUrl.protocol === 'https:' ? https : http;

const req = client.get(targetUrl, options, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    if (res.statusCode === 200) {
      console.log(data);
    } else {
      try {
        const errorData = JSON.parse(data);
        console.error(JSON.stringify({ error: `服务器返回错误 (${res.statusCode}): ${errorData.detail || '未知错误'}` }));
      } catch (e) {
        console.error(JSON.stringify({ error: `服务器返回异常状态码: ${res.statusCode}` }));
      }
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error(JSON.stringify({ error: `请求失败: ${e.message}` }));
  process.exit(1);
});

req.end();
