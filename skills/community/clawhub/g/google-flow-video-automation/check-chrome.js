#!/usr/bin/env node
/**
 * check-chrome.js - 检查 Chrome CDP 连接状态
 * 
 * 功能：
 * 1. 检查 9222 端口是否可访问
 * 2. 检查是否已登录 Google Flow
 * 3. 给出友好的提示和指导
 */

const http = require('http');

console.log('🔍 检查 Chrome CDP 连接状态...\n');

// 检查 9222 端口
function checkCDPPort() {
  return new Promise((resolve, reject) => {
    const req = http.get('http://127.0.0.1:9222/json/version', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const info = JSON.parse(data);
          console.log('✅ Chrome CDP 连接正常！');
          console.log(`   浏览器: ${info['Browser']}`);
          console.log(`   协议版本: ${info['Protocol-Version']}\n`);
          resolve(info);
        } catch (e) {
          reject(new Error('无法解析 CDP 响应'));
        }
      });
    });
    
    req.on('error', (err) => {
      console.log('❌ Chrome CDP 连接失败！\n');
      console.log('💡 可能原因：');
      console.log('   1. Chrome 没有启动');
      console.log('   2. Chrome 启动时没有加 --remote-debugging-port=9222 参数');
      console.log('   3. 端口被其他程序占用\n');
      
      console.log('🚀 解决方案：');
      console.log('   复制以下命令到终端执行：\n');
      console.log('   pkill -9 "Google Chrome"');
      console.log('   sleep 2');
      console.log('   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\');
      console.log('     --remote-debugging-port=9222 \\');
      console.log('     --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default" \\');
      console.log('     "https://labs.google/fx/tools/flow" &\n');
      
      console.log('   然后等待 Chrome 打开（约 5 秒），再运行此脚本检查。\n');
      reject(err);
    });
  });
}

// 主函数
async function main() {
  try {
    const info = await checkCDPPort();
    
    console.log('🎉 太好了！Chrome 已经准备好，可以开始使用 Google Flow 自动化了！');
    console.log('');
    console.log('📋 下一步：');
    console.log('   如果是第一次使用，请运行：node explore-options.js');
    console.log('   如果已经探索过选项，请运行：node generate-one.js --prompt "你的提示词"');
    
  } catch (err) {
    console.log('');
    console.log('⚠️  请先按照上述解决方案启动 Chrome，然后再试一次。');
    process.exit(1);
  }
}

main();
