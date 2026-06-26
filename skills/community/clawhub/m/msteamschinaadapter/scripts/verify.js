/**
 * MSTeams China Patch - 验证脚本
 * 
 * 验证补丁是否正确应用
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 颜色输出
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(color, ...args) {
  console.log(colors[color] || '', ...args, colors.reset);
}

// 检测 dist 路径
function detectDistPath() {
  const candidates = [
    process.env.OPENCLAW_DIST,
    path.join(process.env.APPDATA || '', 'npm', 'node_modules', 'openclaw', 'dist'),
    path.join(process.cwd(), 'node_modules', 'openclaw', 'dist'),
    path.join(os.homedir(), '.nvm', 'versions', 'node', process.version, 'lib', 'node_modules', 'openclaw', 'dist'),
    '/usr/local/lib/node_modules/openclaw/dist',
    '/usr/lib/node_modules/openclaw/dist',
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (candidate && fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return null;
}

// 主函数
function verify() {
  console.log('='.repeat(60));
  log('bold', '✅ MSTeams China Patch - 验证报告');
  console.log('='.repeat(60));
  console.log();

  const distPath = detectDistPath();
  if (!distPath) {
    log('red', '❌ 未找到 dist 目录');
    return { success: false, error: 'dist not found' };
  }

  console.log(`dist 路径: ${distPath}`);
  console.log();

  const files = fs.readdirSync(distPath).filter(f => f.endsWith('.js') && !f.endsWith('.map'));
  let allContent = '';

  for (const file of files) {
    allContent += fs.readFileSync(path.join(distPath, file), 'utf8');
  }

  // 验证项
  const checks = [
    { pattern: 'login.chinacloudapi.cn', name: '中国区 AAD Authority', required: true },
    { pattern: 'api.botframework.azure.cn', name: '中国区 Bot API', required: true },
    { pattern: 'login.botframework.azure.cn', name: '中国区 Bot Login', required: true },
    { pattern: 'token.botframework.azure.cn', name: '中国区 Bot Token', required: true },
    { pattern: 'microsoftgraph.chinacloudapi.cn', name: '中国区 Graph API', required: true },
  ];

  // SSRF Allowlist 验证
  const ssrfChecks = [
    { pattern: 'DEFAULT_MEDIA_HOST_ALLOWLIST', name: '媒体主机允许列表', required: true },
    { pattern: 'DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST', name: '认证主机允许列表', required: true },
  ];

  // 残留检查
  const globalChecks = [
    { pattern: 'login.microsoftonline.com/common/discovery', name: 'Discovery 端点', exclude: 'login.chinacloudapi.cn/common/discovery' },
    { pattern: 'login.botframework.com/v1/.well-known/keys', name: 'JWKS 端点', exclude: 'login.botframework.azure.cn' },
  ];

  log('blue', '📋 端点验证');
  console.log('-'.repeat(40));

  const results = [];
  let allPassed = true;

  for (const check of checks) {
    const found = allContent.includes(check.pattern);
    const status = found ? `${colors.green}✅` : (check.required ? `${colors.red}❌` : `${colors.yellow}⚠️`);
    console.log(`  ${status} ${check.name}${colors.reset}`);
    results.push({ ...check, found });
    if (check.required && !found) allPassed = false;
  }

  console.log();
  log('blue', '🔍 残留检查');
  console.log('-'.repeat(40));

  for (const check of globalChecks) {
    const hasGlobal = allContent.includes(check.pattern);
    const hasChina = allContent.includes(check.exclude);
    
    if (hasGlobal && !hasChina) {
      console.log(`  ${colors.red}❌ ${check.name}: 全球端点未替换${colors.reset}`);
      allPassed = false;
    } else if (hasGlobal && hasChina) {
      console.log(`  ${colors.green}✅ ${check.name}: 中国端点已配置${colors.reset}`);
    } else {
      console.log(`  ${colors.green}✅ ${check.name}: 正常${colors.reset}`);
    }
  }

  console.log();
  log('blue', '🛡️ SSRF Allowlist 验证');
  console.log('-'.repeat(40));

  // 检查 SSRF Allowlist 是否包含中国端点
  for (const check of ssrfChecks) {
    const found = allContent.includes(check.pattern);
    if (found) {
      console.log(`  ${colors.green}✅ ${check.name} 存在${colors.reset}`);
      // 进一步检查是否包含中国端点
      if (allContent.includes('"microsoftgraph.chinacloudapi.cn"')) {
        console.log(`  ${colors.green}✅ 包含 microsoftgraph.chinacloudapi.cn${colors.reset}`);
      } else {
        console.log(`  ${colors.red}❌ 未包含 microsoftgraph.chinacloudapi.cn${colors.reset}`);
        allPassed = false;
      }
    } else {
      console.log(`  ${colors.red}❌ ${check.name} 不存在${colors.reset}`);
      allPassed = false;
    }
  }

  console.log();
  log('blue', '📊 验证结果');
  console.log('-'.repeat(40));

  if (allPassed) {
    log('green', '✅ 所有验证项通过');
    console.log('\n下一步:');
    console.log('  1. 重启 Gateway: openclaw gateway restart');
    console.log('  2. 在 Teams 中测试 Bot 响应');
  } else {
    log('red', '❌ 验证失败');
    console.log('\n建议操作:');
    console.log('  1. 重新运行: node scripts/apply_patch.js');
    console.log('  2. 再次验证: node scripts/verify.js');
  }

  console.log();
  console.log('='.repeat(60));

  return { success: allPassed, results };
}

// 导出
module.exports = { verify, detectDistPath };

// 执行
if (require.main === module) {
  verify();
}