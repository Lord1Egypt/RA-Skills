#!/usr/bin/env node

/**
 * 企业微信配置验证工具
 * 检查企业微信接收消息服务器配置是否完整
 */

const fs = require('fs');
const path = require('path');

function validateWeChatConfig() {
  console.log('🔍 验证企业微信接收消息服务器配置...\n');
  
  // 检查配置文件是否存在
  let configPath = path.join(__dirname, '..', '..', 'openclaw.json');
  
  // 如果找不到，尝试从工作区根目录查找
  if (!fs.existsSync(configPath)) {
    const altConfigPath = path.join(__dirname, '..', '..', '..', 'openclaw.json');
    if (fs.existsSync(altConfigPath)) {
      configPath = altConfigPath;
    }
  }
  
  if (!fs.existsSync(configPath)) {
    console.error('❌ 配置文件不存在: openclaw.json');
    return false;
  }
  
  // 读取配置文件
  let config;
  try {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  } catch (error) {
    console.error('❌ 配置文件格式错误:', error.message);
    return false;
  }
  
  // 检查企业微信配置
  const wechatConfig = config.channels?.wecom;
  
  if (!wechatConfig) {
    console.error('❌ 配置文件中缺少 wechat 配置');
    return false;
  }
  
  console.log('📋 企业微信配置检查结果:\n');
  
  // 必需字段检查
  const requiredFields = ['enabled', 'url', 'token', 'encodingAesKey'];
  const optionalFields = ['adminUsers', 'commands', 'dynamicAgents', 'workspaceTemplate', 'agent'];
  
  console.log('🔸 必需字段检查:');
  let allRequiredFieldsValid = true;
  
  for (const field of requiredFields) {
    if (wechatConfig[field]) {
      if (field === 'url') {
        // 特殊处理URL格式验证
        try {
          const url = new URL(wechatConfig[field]);
          if (url.protocol !== 'https:') {
            console.log(`  ❌ ${field}: 必须使用HTTPS协议`);
            allRequiredFieldsValid = false;
          } else if (!wechatConfig[field].includes('/webhooks/wecom')) {
            console.log(`  ⚠️  ${field}: 建议使用包含 /webhooks/wecom 的路径`);
          } else {
            console.log(`  ✅ ${field}: ${wechatConfig[field]}`);
          }
        } catch (error) {
          console.log(`  ❌ ${field}: URL格式无效`);
          allRequiredFieldsValid = false;
        }
      } else if (field === 'encodingAesKey') {
        // 检查EncodingAESKey长度
        if (wechatConfig[field].length !== 43) {
          console.log(`  ❌ ${field}: 必须是43位字符，当前长度: ${wechatConfig[field].length}`);
          allRequiredFieldsValid = false;
        } else {
          console.log(`  ✅ ${field}: 长度正确 (${wechatConfig[field].length}位)`);
        }
      } else {
        console.log(`  ✅ ${field}: 已配置`);
      }
    } else {
      console.log(`  ❌ ${field}: 未配置`);
      allRequiredFieldsValid = false;
    }
  }
  
  console.log('\n🔸 可选字段检查:');
  let hasOptionalConfig = false;
  
  for (const field of optionalFields) {
    if (wechatConfig[field]) {
      console.log(`  ✅ ${field}: 已配置`);
      hasOptionalConfig = true;
      
      // 特殊检查agent配置
      if (field === 'agent') {
        const agent = wechatConfig[field];
        const agentRequired = ['corpId', 'corpSecret', 'agentId'];
        
        console.log('    🔸 Agent配置检查:');
        for (const agentField of agentRequired) {
          if (agent[agentField]) {
            console.log(`      ✅ ${agentField}: 已配置`);
          } else {
            console.log(`      ❌ ${agentField}: 未配置`);
          }
        }
      }
    } else {
      console.log(`  ⚠️  ${field}: 未配置（可选）`);
    }
  }
  
  // 生成配置建议
  console.log('\n💡 配置建议:\n');
  
  if (!allRequiredFieldsValid) {
    console.log('1. 请确保配置所有必需字段');
    console.log('2. 检查URL格式是否正确（必须是HTTPS）');
    console.log('3. 确认EncodingAESKey长度为43位');
    console.log('4. 确保回调地址可以从企业微信访问');
  }
  
  if (allRequiredFieldsValid) {
    console.log('✅ 基本配置验证通过');
    console.log('📝 下一步操作:');
    console.log('1. 登录企业微信管理后台');
    console.log('2. 进入应用设置');
    console.log('3. 配置接收消息服务器:');
    console.log('   - URL: ' + wechatConfig.url);
    console.log('   - Token: ' + wechatConfig.token);
    console.log('   - EncodingAESKey: ' + wechatConfig.encodingAesKey);
    console.log('4. 保存配置');
  }
  
  console.log('\n🔧 故障排查:');
  console.log('- 如果保存失败，请检查服务器是否可以从公网访问');
  console.log('- 确认SSL证书有效');
  console.log('- 检查防火墙是否放行企业微信服务器IP');
  
  return allRequiredFieldsValid;
}

// 如果直接运行此脚本
if (require.main === module) {
  const isValid = validateWeChatConfig();
  
  if (isValid) {
    console.log('\n✅ 企业微信配置验证通过');
    console.log('🧪 可以尝试保存企业微信后台配置了');
  } else {
    console.log('\n❌ 配置验证失败，请检查配置');
    process.exit(1);
  }
}

module.exports = { validateWeChatConfig };