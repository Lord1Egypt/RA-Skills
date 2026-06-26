/**
 * 为多维表格添加编辑权限
 * 用法: node add_permission.js --open-id "USER_OPEN_ID" --perm "edit|view|full_access"
 * 
 * 功能：
 * 1. 获取 tenant_access_token
 * 2. 将指定用户添加为多维表格的编辑者
 * 
 * 使用 request.js 统一请求（带重试/超时/401自动刷新）
 */

const { getAccessToken } = require('./request');
const { CONFIG } = require('./config');
const { getLanguage, getTemplates } = require('./i18n');

// 权限级别
const PERM_LEVELS = {
  view: 'view',
  edit: 'edit',
  full_access: 'full_access'
};

async function addPermission(openId, perm = 'edit') {
  const token = await getAccessToken();
  const lang = getLanguage();
  const t = getTemplates(lang);

  console.log(t.permission?.adding || '🔄 添加多维表格编辑权限...');
  console.log(`   Open ID: ${openId}`);
  console.log(`   Permission: ${perm}`);

  try {
    const response = await require('axios').post(
      `https://open.feishu.cn/open-apis/drive/v1/permissions/${CONFIG.APP_TOKEN}/members?type=bitable`,
      {
        member_type: 'openid',
        member_id: openId,
        perm: PERM_LEVELS[perm] || 'edit'
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      }
    );

    if (response.data.code === 0) {
      console.log('✅ ' + (t.permission?.success || '权限添加成功'));
      return { success: true };
    } else {
      console.error('❌ ' + (t.permission?.failed || '权限添加失败') + `: ${response.data.msg}`);
      return { success: false, msg: response.data.msg };
    }
  } catch (error) {
    const errMsg = error.response?.data?.msg || error.message;
    console.error('❌ ' + (t.permission?.error || '权限添加异常') + `: ${errMsg}`);
    return { success: false, error: errMsg };
  }
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  let openId = null;
  let perm = 'edit';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--open-id' && args[i + 1]) {
      openId = args[i + 1];
      i++;
    } else if (args[i] === '--perm' && args[i + 1]) {
      perm = args[i + 1];
      i++;
    } else if (args[i] === '--lang' && args[i + 1]) {
      // 语言参数会被 i18n 自动识别，这里忽略
      i++;
    }
  }

  // 如果没有传 open-id，使用配置中的默认用户ID
  if (!openId) {
    console.log('⚠️  未指定 --open-id，尝试从配置读取...');
    // 这里可以从配置文件读取默认用户ID，暂用占位符
    console.log('❌ 请通过 --open-id 参数指定用户 Open ID');
    console.log('   用法: node add_permission.js --open-id "USER_OPEN_ID" --perm "edit"');
    process.exit(1);
  }

  const result = await addPermission(openId, perm);
  process.exit(result.success ? 0 : 1);
}

// 只在直接运行时执行 main()，被 require 时不执行
if (require.main === module) {
  main();
}

module.exports = { addPermission };
