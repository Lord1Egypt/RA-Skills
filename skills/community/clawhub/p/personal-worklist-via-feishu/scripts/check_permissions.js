/**
 * 检查飞书 API 连通性
 * 用法: node check_permissions.js
 * 
 * 需要先在 config.js 中配置 APP_ID 和 APP_SECRET
 */

const axios = require('axios');
const { CONFIG } = require('./config');

async function checkPermissions() {
  console.log('🔄 检查飞书 API 连通性...');
  
  try {
    const response = await axios.post(
      'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
      {
        app_id: CONFIG.APP_ID,
        app_secret: CONFIG.APP_SECRET
      },
      { timeout: 10000 }  // 10秒超时控制
    );
    
    if (response.data.tenant_access_token) {
      console.log('✅ API 连通性正常');
      console.log('   Token 获取成功');
      return { success: true, token: response.data.tenant_access_token };
    }
  } catch (error) {
    console.error('❌ API 连通性检查失败:', error.response?.data?.msg || error.message);
    return { success: false, error: error.response?.data || error.message };
  }
}

async function main() {
  const result = await checkPermissions();
  if (!result.success) {
    process.exit(1);
  }
}

main();