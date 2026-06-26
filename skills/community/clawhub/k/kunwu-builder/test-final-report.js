#!/usr/bin/env node

/**
 * 最终测试报告 - 总结装配功能测试结果
 */

import http from 'http';

const BASE_URL = 'http://100.85.119.45:16888';

function callAPI(endpoint, data) {
  return new Promise((resolve, reject) => {
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
        try {
          resolve(JSON.parse(responseData));
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

async function finalReport() {
  console.log('📊 装配功能测试 - 最终报告\n');
  console.log('=' .repeat(60));
  
  // 1. 查看场景中的模型
  console.log('\n1️⃣ 场景中的模型:');
  const allInfo = await callAPI('/GetAllModelInfo', {});
  const models = allInfo.data?.models || [];
  
  models.forEach((m, i) => {
    console.log(`   ${i+1}. ${m.modelName} (${m.modelId})`);
  });
  
  // 2. 查看本地模型库
  console.log('\n2️⃣ 本地模型库:');
  const localResult = await callAPI('/model/library/local', {});
  const localModels = localResult.data?.models || [];
  
  localModels.forEach((m, i) => {
    console.log(`   ${i+1}. ${m.modelName}`);
    console.log(`      路径：${m.relativePath}`);
  });
  
  // 3. 测试结论
  console.log('\n' + '=' .repeat(60));
  console.log('📋 测试结论\n');
  
  console.log('✅ 成功:');
  console.log('   - Dufault 2D 相机可以从本地模型库下载');
  console.log('   - /model/assemble API 可用（需要正确的模型类型）');
  console.log('   - /model/set_parent 可以建立父子关系\n');
  
  console.log('❌ 失败:');
  console.log('   - Camera Bracket 从本地模型库下载失败');
  console.log('   - 原因：模型文件可能损坏或路径配置问题');
  console.log('   - 远程模型库搜索返回 0 结果\n');
  
  console.log('🔑 关键发现:');
  console.log('   - /model/assemble 需要模型有预定义装配位');
  console.log('   - 参数化模型（方形、圆柱）不支持装配');
  console.log('   - 必须使用真实的设备模型（机器人、相机支架等）\n');
  
  console.log('💡 建议:');
  console.log('   1. 检查 Kunwu Builder 的本地模型库配置');
  console.log('   2. 确认 Camera Bracket.rtprefab 文件存在且完整');
  console.log('   3. 或者从 Kunwu 官方重新下载模型库');
  console.log('   4. 临时方案：使用 /model/set_parent 建立层级关系\n');
  
  console.log('=' .repeat(60));
}

finalReport().catch(console.error);
