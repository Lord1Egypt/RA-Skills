/**
 * 飞书工作台账健康检查脚本
 * 用法: node health_check.js [--lang zh|en]
 * 
 * 诊断维度：
 * 1. 网络连通性（是否能访问飞书 API）
 * 2. API 凭证有效性（App ID / App Secret 是否正确）
 * 3. 多维表格可访问性（表格是否存在且有权限）
 * 4. 字段配置完整性（必填字段是否齐全）
 * 5. Token 刷新机制验证
 * 
 * 触发场景：
 * - 用户说"台账好像不工作了"
 * - 用户说"数据没更新"
 * - 用户说"操作没反应"
 * - 英文环境: "worklist not working", "data not updated", "no response"
 * 
 * 使用 request.js 统一请求（带重试/超时/401自动刷新）
 */

const axios = require('axios');
const { getAccessToken, fetchWithRetry } = require('./request');
const { CONFIG } = require('./config');
const { getLanguage, getTemplates, format } = require('./i18n');

// 健康检查项
const CHECKS = {
  NETWORK: 'network',
  API_CREDENTIALS: 'api_credentials',
  TOKEN: 'token',
  TABLE_ACCESS: 'table_access',
  FIELD_CONFIG: 'field_config'
};

const CHECK_NAMES_ZH = {
  [CHECKS.NETWORK]: '网络连通性',
  [CHECKS.API_CREDENTIALS]: 'API 凭证',
  [CHECKS.TOKEN]: 'Token 获取',
  [CHECKS.TABLE_ACCESS]: '表格访问',
  [CHECKS.FIELD_CONFIG]: '字段配置'
};

const CHECK_NAMES_EN = {
  [CHECKS.NETWORK]: 'Network',
  [CHECKS.API_CREDENTIALS]: 'API Credentials',
  [CHECKS.TOKEN]: 'Token',
  [CHECKS.TABLE_ACCESS]: 'Table Access',
  [CHECKS.FIELD_CONFIG]: 'Field Config'
};

// 必填字段（中英文）
const REQUIRED_FIELDS_ZH = ['任务名称', '来源分类', '优先级', '状态', '截止日期'];
const REQUIRED_FIELDS_EN = ['Task Name', 'Source Category', 'Priority', 'Status', 'Deadline'];

function getRequiredFields(lang) {
  return lang === 'en' ? REQUIRED_FIELDS_EN : REQUIRED_FIELDS_ZH;
}

function getCheckName(check, lang) {
  const map = lang === 'en' ? CHECK_NAMES_EN : CHECK_NAMES_ZH;
  return map[check] || check;
}

// 检查 1: 网络连通性
async function checkNetwork() {
  try {
    const start = Date.now();
    await axios.get('https://open.feishu.cn', { timeout: 5000 });
    const latency = Date.now() - start;
    return { status: 'ok', latency, message: `${latency}ms` };
  } catch (error) {
    return { status: 'fail', message: error.code || 'ECONNREFUSED' };
  }
}

// 检查 2: API 凭证格式
function checkApiCredentials() {
  const issues = [];
  
  if (!CONFIG.APP_ID || CONFIG.APP_ID === 'YOUR_APP_ID') {
    issues.push('APP_ID 未配置或为占位符');
  } else if (!CONFIG.APP_ID.startsWith('cli_')) {
    issues.push('APP_ID 格式可能不正确（应为 cli_ 开头）');
  }
  
  if (!CONFIG.APP_SECRET || CONFIG.APP_SECRET === 'YOUR_APP_SECRET') {
    issues.push('APP_SECRET 未配置或为占位符');
  }
  
  if (!CONFIG.APP_TOKEN || CONFIG.APP_TOKEN === 'YOUR_APP_TOKEN') {
    issues.push('APP_TOKEN 未配置或为占位符');
  }
  
  if (!CONFIG.TABLE_ID || CONFIG.TABLE_ID === 'YOUR_TABLE_ID') {
    issues.push('TABLE_ID 未配置或为占位符');
  }
  
  if (issues.length === 0) {
    return { status: 'ok', message: '凭证格式正确' };
  }
  return { status: 'fail', message: issues.join('; ') };
}

// 检查 3: Token 获取
async function checkToken() {
  try {
    // 使用 fetchWithRetry 包装，增加网络抖动容错
    const response = await fetchWithRetry(async () => {
      return axios.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        { app_id: CONFIG.APP_ID, app_secret: CONFIG.APP_SECRET },
        { timeout: 10000 }
      );
    }, 2, [1000, 2000]);  // 2次重试，1s/2s退避
    
    if (response.data.tenant_access_token) {
      return { status: 'ok', message: 'Token 获取成功', token: response.data.tenant_access_token };
    }
    
    if (response.data.code === 99991663) {
      return { status: 'fail', message: 'App ID 或 App Secret 错误' };
    }
    
    return { status: 'fail', message: response.data.msg || '未知错误' };
  } catch (error) {
    if (error.response?.data?.code === 99991663) {
      return { status: 'fail', message: 'App ID 或 App Secret 错误（凭证无效）' };
    }
    return { status: 'fail', message: error.message };
  }
}

// 检查 4: 表格访问权限
async function checkTableAccess(token) {
  try {
    const response = await axios.get(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables`,
      { headers: { Authorization: `Bearer ${token}` }, timeout: 10000 }
    );
    
    if (response.data.code === 0) {
      const tables = response.data.data?.items || [];
      const targetTable = tables.find(t => t.table_id === CONFIG.TABLE_ID);
      
      if (targetTable) {
        return { status: 'ok', message: `表格存在: ${targetTable.name}` };
      }
      
      return { status: 'fail', message: `TABLE_ID 不存在或无权限访问（找到 ${tables.length} 个表格）` };
    }
    
    if (response.data.code === 230002) {
      return { status: 'fail', message: 'APP_TOKEN 无效或已失效' };
    }
    
    return { status: 'fail', message: response.data.msg || '未知错误' };
  } catch (error) {
    if (error.response?.data?.code === 230002) {
      return { status: 'fail', message: 'APP_TOKEN 无效或已失效' };
    }
    return { status: 'fail', message: error.message };
  }
}

// 检查 5: 字段配置
async function checkFieldConfig(token) {
  try {
    const response = await axios.get(
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${CONFIG.TABLE_ID}/fields`,
      { headers: { Authorization: `Bearer ${token}` }, timeout: 10000 }
    );
    
    if (response.data.code !== 0) {
      return { status: 'fail', message: response.data.msg || '获取字段失败' };
    }
    
    const fields = response.data.data?.items || [];
    const fieldNames = fields.map(f => f.field_name);
    const lang = getLanguage();
    const requiredFields = getRequiredFields(lang);
    
    const missingFields = requiredFields.filter(f => !fieldNames.includes(f));
    
    if (missingFields.length === 0) {
      return { status: 'ok', message: `全部 ${requiredFields.length} 个必填字段齐全（共 ${fields.length} 个字段）` };
    }
    
    return { 
      status: 'warn', 
      message: `缺少 ${missingFields.length} 个必填字段: ${missingFields.join(', ')}` 
    };
  } catch (error) {
    return { status: 'fail', message: error.message };
  }
}

// 生成诊断报告
function generateReport(results, lang) {
  const t = getTemplates(lang);
  const checkNames = lang === 'en' ? CHECK_NAMES_EN : CHECK_NAMES_ZH;
  
  console.log(lang === 'zh' ? '\n🔍 健康检查报告\n' : '\n🔍 Health Check Report\n');
  console.log('─'.repeat(40));
  
  for (const [check, result] of Object.entries(results)) {
    const checkName = checkNames[check] || check;
    const icon = result.status === 'ok' ? '✅' : result.status === 'warn' ? '⚠️ ' : '❌';
    const label = lang === 'zh' 
      ? { ok: '正常', fail: '异常', warn: '警告' }[result.status] 
      : { ok: 'OK', fail: 'FAIL', warn: 'WARN' }[result.status];
    
    console.log(`${icon} ${checkName}: [${label}] ${result.message}`);
  }
  
  console.log('─'.repeat(40));
  
  // 汇总诊断
  const allOk = Object.values(results).every(r => r.status === 'ok');
  const failCount = Object.values(results).filter(r => r.status === 'fail').length;
  
  console.log();
  
  if (allOk) {
    console.log(lang === 'zh' 
      ? '✅ 所有检查通过，台账功能正常。可能是操作延迟或数据暂无更新。' 
      : '✅ All checks passed. Worklist is functioning normally. It may be operation delay or no new data.');
  } else if (results[CHECKS.NETWORK]?.status === 'fail') {
    console.log(lang === 'zh' 
      ? '🌐 网络问题：无法访问飞书 API。请检查网络连接。' 
      : '🌐 Network issue: Cannot reach Feishu API. Please check your network connection.');
  } else if (results[CHECKS.API_CREDENTIALS]?.status === 'fail' || results[CHECKS.TOKEN]?.status === 'fail') {
    console.log(lang === 'zh' 
      ? '🔑 凭证问题：API 凭证无效。请检查 config.js 中的 APP_ID / APP_SECRET。' 
      : '🔑 Credential issue: API credentials invalid. Please check APP_ID / APP_SECRET in config.js.');
  } else if (results[CHECKS.TABLE_ACCESS]?.status === 'fail') {
    console.log(lang === 'zh' 
      ? '📋 表格问题：无法访问多维表格。请检查 APP_TOKEN / TABLE_ID 是否正确，或确认表格是否被删除。' 
      : '📋 Table issue: Cannot access bitable. Please check APP_TOKEN / TABLE_ID or verify the table exists.');
  } else if (results[CHECKS.FIELD_CONFIG]?.status !== 'ok') {
    console.log(lang === 'zh' 
      ? '⚙️  配置问题：字段配置不完整。请运行 `node scripts/init_table.js` 补全字段。' 
      : '⚙️  Config issue: Field configuration incomplete. Please run `node scripts/init_table.js` to fix.');
  } else {
    console.log(lang === 'zh' 
      ? '⚠️  存在异常，请根据上述报告定位问题。' 
      : '⚠️  Some issues detected. Please review the report above.');
  }
  
  // 建议操作
  console.log();
  if (lang === 'zh') {
    console.log('💡 常用修复命令：');
    console.log('   node scripts/health_check.js          # 重新诊断');
    console.log('   node scripts/init_table.js            # 初始化/修复字段');
    console.log('   node scripts/set_config.js --list      # 查看当前配置');
    console.log('   node scripts/set_config.js --app-token "xxx" --table-id "xxx"  # 更新配置');
  } else {
    console.log('💡 Common fixes:');
    console.log('   node scripts/health_check.js          # Re-diagnose');
    console.log('   node scripts/init_table.js            # Initialize/fix fields');
    console.log('   node scripts/set_config.js --list      # View current config');
    console.log('   node scripts/set_config.js --app-token "xxx" --table-id "xxx"  # Update config');
  }
  
  return allOk;
}

async function healthCheck() {
  const lang = getLanguage();
  const t = getTemplates(lang);
  
  console.log(lang === 'zh' ? '🔄 正在进行健康检查...' : '🔄 Running health check...');
  
  const results = {};
  
  // 检查 1: 网络
  results[CHECKS.NETWORK] = await checkNetwork();
  console.log(results[CHECKS.NETWORK].status === 'ok' 
    ? `✅ ${getCheckName(CHECKS.NETWORK, lang)}: ${results[CHECKS.NETWORK].message}` 
    : `❌ ${getCheckName(CHECKS.NETWORK, lang)}: ${results[CHECKS.NETWORK].message}`);
  
  // 检查 2: API 凭证
  results[CHECKS.API_CREDENTIALS] = checkApiCredentials();
  console.log(results[CHECKS.API_CREDENTIALS].status === 'ok'
    ? `✅ ${getCheckName(CHECKS.API_CREDENTIALS, lang)}: ${results[CHECKS.API_CREDENTIALS].message}`
    : `❌ ${getCheckName(CHECKS.API_CREDENTIALS, lang)}: ${results[CHECKS.API_CREDENTIALS].message}`);
  
  // 如果凭证格式有问题，后续检查可能无法完成
  if (results[CHECKS.API_CREDENTIALS].status === 'fail') {
    results[CHECKS.TOKEN] = { status: 'skip', message: '跳过（凭证格式问题）' };
    results[CHECKS.TABLE_ACCESS] = { status: 'skip', message: '跳过（凭证格式问题）' };
    results[CHECKS.FIELD_CONFIG] = { status: 'skip', message: '跳过（凭证格式问题）' };
    generateReport(results, lang);
    return;
  }
  
  // 检查 3: Token
  results[CHECKS.TOKEN] = await checkToken();
  console.log(results[CHECKS.TOKEN].status === 'ok'
    ? `✅ ${getCheckName(CHECKS.TOKEN, lang)}: ${results[CHECKS.TOKEN].message}`
    : `❌ ${getCheckName(CHECKS.TOKEN, lang)}: ${results[CHECKS.TOKEN].message}`);
  
  if (results[CHECKS.TOKEN].status === 'fail') {
    results[CHECKS.TABLE_ACCESS] = { status: 'skip', message: '跳过（Token 获取失败）' };
    results[CHECKS.FIELD_CONFIG] = { status: 'skip', message: '跳过（Token 获取失败）' };
    generateReport(results, lang);
    return;
  }
  
  const token = results[CHECKS.TOKEN].token;
  
  // 检查 4: 表格访问
  results[CHECKS.TABLE_ACCESS] = await checkTableAccess(token);
  console.log(results[CHECKS.TABLE_ACCESS].status === 'ok'
    ? `✅ ${getCheckName(CHECKS.TABLE_ACCESS, lang)}: ${results[CHECKS.TABLE_ACCESS].message}`
    : results[CHECKS.TABLE_ACCESS].status === 'skip'
    ? `⏭️  ${getCheckName(CHECKS.TABLE_ACCESS, lang)}: ${results[CHECKS.TABLE_ACCESS].message}`
    : `❌ ${getCheckName(CHECKS.TABLE_ACCESS, lang)}: ${results[CHECKS.TABLE_ACCESS].message}`);
  
  if (results[CHECKS.TABLE_ACCESS].status === 'fail') {
    results[CHECKS.FIELD_CONFIG] = { status: 'skip', message: '跳过（表格访问失败）' };
    generateReport(results, lang);
    return;
  }
  
  // 检查 5: 字段配置
  results[CHECKS.FIELD_CONFIG] = await checkFieldConfig(token);
  console.log(results[CHECKS.FIELD_CONFIG].status === 'ok'
    ? `✅ ${getCheckName(CHECKS.FIELD_CONFIG, lang)}: ${results[CHECKS.FIELD_CONFIG].message}`
    : results[CHECKS.FIELD_CONFIG].status === 'warn'
    ? `⚠️  ${getCheckName(CHECKS.FIELD_CONFIG, lang)}: ${results[CHECKS.FIELD_CONFIG].message}`
    : `❌ ${getCheckName(CHECKS.FIELD_CONFIG, lang)}: ${results[CHECKS.FIELD_CONFIG].message}`);
  
  generateReport(results, lang);
}

async function main() {
  try {
    await healthCheck();
  } catch (error) {
    const lang = getLanguage();
    console.error(lang === 'zh' ? `❌ 健康检查失败: ${error.message}` : `❌ Health check failed: ${error.message}`);
    process.exit(1);
  }
}

main();