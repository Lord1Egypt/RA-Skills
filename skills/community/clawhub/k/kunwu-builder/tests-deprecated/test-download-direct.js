#!/usr/bin/env node

/**
 * 直接调用下载 API 查看错误
 */

import http from 'http';

const BASE_URL = 'http://100.85.119.45:16888';

function callAPI(endpoint, data) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, BASE_URL);
    const body = JSON.stringify(data);
    
    const options = {
      hostname: new URL(BASE_URL).hostname,
      port: new URL(BASE_URL).port,
      path: endpoint,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = http.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      res.on('end', () => {
        console.log(`HTTP ${res.statusCode} 响应:`);
        console.log(responseData);
        
        try {
          const result = JSON.parse(responseData);
          resolve(result);
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`Connection error: ${e.message}`));
    });

    req.write(body);
    req.end();
  });
}

async function testDownload() {
  console.log('📥 直接调用下载 API\n');
  
  // 测试 1: 使用 modelName
  console.log('测试 1: 使用 modelName="Camera Bracket"');
  const result1 = await callAPI('/model/download', {
    id: 'Camera Bracket',
    createInScene: true,
    position: [0, 0, 0],
    rename: '测试_支架_1'
  });
  console.log('结果:', JSON.stringify(result1, null, 2));
  
  // 测试 2: 使用 relativePath
  console.log('\n\n测试 2: 使用 relativePath');
  const result2 = await callAPI('/model/download', {
    relativePath: 'CloudModel/Camera/Camera Bracket/Camera Bracket.rtprefab',
    createInScene: true,
    position: [0, 0, 100],
    rename: '测试_支架_2'
  });
  console.log('结果:', JSON.stringify(result2, null, 2));
}

testDownload().catch(console.error);
