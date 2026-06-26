#!/usr/bin/env node

/**
 * 企业微信配置验证工具
 * 检查配置文件是否完整和正确
 */

const fs = require('fs');
const path = require('path');

function validateWeChatConfig() {
  console.log('🔍 验证企业微信配置...\n');
  
  // 检查配置文件是否存在
  const configPath = path.join(__dirname, 'config.json');
  
  if (!fs.existsSync(configPath)) {
    console.error('❌ 配置文件不存在: config.json');
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
  const wechatConfig = config.wechatWork;
  
  if (!wechatConfig) {
    console.error('❌ 配置文件中缺少 wechatWork 配置段');
    return false;
  }
  
  console.log('📋 配置检查结果:\n');
  
  // 必需字段检查
  const requiredFields = ['webhookUrl'];
  const optionalFields = ['smartTableId', 'departmentId', 'apiToken', 'corpId', 'corpSecret', 'token', 'encodingAESKey'];
  
  console.log('🔸 必需字段检查:');
  let allRequiredFieldsValid = true;
  
  for (const field of requiredFields) {
    if (wechatConfig[field]) {
      console.log(`  ✅ ${field}: 已配置`);
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
    } else {
      console.log(`  ⚠️  ${field}: 未配置（可选）`);
    }
  }
  
  // 验证Webhook URL格式
  if (wechatConfig.webhookUrl) {
    console.log('\n🔸 Webhook URL验证:');
    
    try {
      const url = new URL(wechatConfig.webhookUrl);
      
      if (url.protocol !== 'https:') {
        console.log('  ❌ URL协议必须是HTTPS');
        allRequiredFieldsValid = false;
      } else {
        console.log('  ✅ URL协议正确（HTTPS）');
      }
      
      if (!url.hostname) {
        console.log('  ❌ URL缺少域名');
        allRequiredFieldsValid = false;
      } else {
        console.log(`  ✅ 域名: ${url.hostname}`);
      }
      
    } catch (error) {
      console.log(`  ❌ URL格式无效: ${error.message}`);
      allRequiredFieldsValid = false;
    }
  }
  
  // 检查智能表格配置
  if (wechatConfig.smartTableId && !wechatConfig.apiToken) {
    console.log('\n⚠️  警告: 配置了智能表格ID但缺少API Token');
  }
  
  // 生成配置建议
  console.log('\n💡 配置建议:\n');
  
  if (!allRequiredFieldsValid) {
    console.log('1. 请确保配置所有必需字段');
    console.log('2. 检查Webhook URL格式是否正确');
    console.log('3. 确认回调地址已添加到企业微信可信域名列表');
  }
  
  if (hasOptionalConfig) {
    console.log('1. 如需使用智能表格功能，请确保配置了正确的表格ID');
    console.log('2. 如需自动获取Token，请配置CorpID和Secret');
    console.log('3. 如需启用回调模式，请配置Token和EncodingAESKey');
  }
  
  console.log('\n📚 详细配置指南请参考: WECHAT_SETUP.md');
  
  return allRequiredFieldsValid;
}

// 如果直接运行此脚本
if (require.main === module) {
  const isValid = validateWeChatConfig();
  
  if (isValid) {
    console.log('\n✅ 基本配置验证通过');
    console.log('🧪 运行测试脚本: node test-wechat.js');
  } else {
    console.log('\n❌ 配置验证失败，请检查配置');
    process.exit(1);
  }
}

module.exports = { validateWeChatConfig };