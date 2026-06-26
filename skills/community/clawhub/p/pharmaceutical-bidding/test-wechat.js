#!/usr/bin/env node

/**
 * 企业微信API测试脚本
 * 用于验证企业微信配置是否正确
 */

const WeChatWorkAPI = require('./wechat-api');
const config = require('./config.json');

async function testWeChatAPI() {
  console.log('🧪 开始测试企业微信API配置...\n');
  
  // 检查配置
  console.log('📋 检查配置文件...');
  const wechatConfig = config.wechatWork;
  
  if (!wechatConfig || Object.keys(wechatConfig).length === 0) {
    console.error('❌ 企业微信配置为空，请先配置 config.json 中的 wechatWork 部分');
    return;
  }
  
  const requiredFields = ['webhookUrl'];
  const missingFields = requiredFields.filter(field => !wechatConfig[field]);
  
  if (missingFields.length > 0) {
    console.error(`❌ 缺少必需的配置字段: ${missingFields.join(', ')}`);
    return;
  }
  
  console.log('✅ 基本配置检查通过');
  
  // 初始化API
  const wechatAPI = new WeChatWorkAPI(wechatConfig);
  
  try {
    // 测试1: 发送文本消息
    console.log('\n📝 测试1: 发送文本消息...');
    await wechatAPI.sendText('测试消息：药学系统招标信息收集系统测试');
    console.log('✅ 文本消息发送成功');
    
    // 测试2: 发送Markdown消息
    console.log('\n📝 测试2: 发送Markdown消息...');
    const markdown = `
## 📋 系统测试通知

**系统名称**: 药学系统招标信息收集系统
**测试时间**: ${new Date().toLocaleString()}
**状态**: 运行正常

---
*此为系统测试消息，请忽略*
    `;
    
    await wechatAPI.sendMarkdown(markdown);
    console.log('✅ Markdown消息发送成功');
    
    // 测试3: 智能表格记录（如果配置了）
    if (wechatConfig.smartTableId) {
      console.log('\n📊 测试3: 智能表格记录...');
      const testData = {
        '测试项目': '系统测试记录',
        '测试时间': new Date().toLocaleString(),
        '状态': '成功',
        '备注': '系统自动测试'
      };
      
      await wechatAPI.recordToSmartTable(testData);
      console.log('✅ 智能表格记录成功');
    } else {
      console.log('\n⚠️  智能表格ID未配置，跳过表格测试');
    }
    
    // 测试4: 获取Access Token（如果配置了CorpID和Secret）
    if (wechatConfig.corpId && wechatConfig.corpSecret) {
      console.log('\n🔑 测试4: 获取Access Token...');
      const token = await wechatAPI.getAccessToken(wechatConfig.corpId, wechatConfig.corpSecret);
      console.log(`✅ Access Token获取成功: ${token.substring(0, 20)}...`);
    } else {
      console.log('\n⚠️  CorpID和Secret未配置，跳过Token测试');
    }
    
    console.log('\n🎉 所有测试通过！企业微信API配置正确');
    
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    console.error('\n🔍 排查建议:');
    
    if (error.message.includes('回调地址请求不通过')) {
      console.error('1. 检查回调地址是否已添加到企业微信可信域名列表');
      console.error('2. 确认回调地址使用HTTPS协议');
      console.error('3. 验证回调地址是否可以正常访问');
      console.error('4. 检查SSL证书是否有效');
    } else if (error.message.includes('errcode')) {
      console.error('1. 检查企业微信应用配置是否正确');
      console.error('2. 确认应用权限是否充足');
      console.error('3. 查看企业微信错误码说明');
    } else {
      console.error('1. 检查网络连接');
      console.error('2. 验证配置参数');
      console.error('3. 查看详细错误信息');
    }
  }
}

// 运行测试
if (require.main === module) {
  testWeChatAPI().catch(console.error);
}

module.exports = { testWeChatAPI };