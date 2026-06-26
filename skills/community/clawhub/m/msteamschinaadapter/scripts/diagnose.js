/**
 * MSTeams China Patch - 诊断脚本
 * 
 * 检查当前环境状态，识别 Teams 中国区配置问题
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

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

  try {
    const npmRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    const distPath = path.join(npmRoot, 'openclaw', 'dist');
    if (fs.existsSync(distPath)) return distPath;
  } catch (e) { }

  return null;
}

// 检查端点配置
function checkEndpoints(distPath) {
  const checks = {
    'login.chinacloudapi.cn': { found: false, count: 0, desc: '中国区 AAD Authority' },
    'api.botframework.azure.cn': { found: false, count: 0, desc: '中国区 Bot API' },
    'login.botframework.azure.cn': { found: false, count: 0, desc: '中国区 Bot Login' },
    'token.botframework.azure.cn': { found: false, count: 0, desc: '中国区 Bot Token' },
    'microsoftgraph.chinacloudapi.cn': { found: false, count: 0, desc: '中国区 Graph API' },
    'login.microsoftonline.com': { found: false, count: 0, desc: '全球 AAD (应替换)', isGlobal: true },
    'api.botframework.com': { found: false, count: 0, desc: '全球 Bot API (应替换)', isGlobal: true },
    'login.botframework.com': { found: false, count: 0, desc: '全球 Bot Login (应替换)', isGlobal: true },
  };

  const files = fs.readdirSync(distPath).filter(f => f.endsWith('.js') && !f.endsWith('.map'));

  for (const file of files) {
    const content = fs.readFileSync(path.join(distPath, file), 'utf8');

    for (const [pattern, info] of Object.entries(checks)) {
      const matches = content.split(pattern).length - 1;
      if (matches > 0) {
        info.found = true;
        info.count += matches;
      }
    }
  }

  return checks;
}

// 主函数
function diagnose() {
  console.log('='.repeat(60));
  log('bold', '🔍 MSTeams China Patch - 诊断报告');
  console.log('='.repeat(60));
  console.log();

  // 1. 环境信息
  log('blue', '📦 环境信息');
  console.log('-'.repeat(40));

  try {
    const version = execSync('openclaw --version', { encoding: 'utf8' }).trim();
    console.log(`OpenClaw 版本: ${version}`);
  } catch (e) {
    log('yellow', 'OpenClaw 版本: 无法获取');
  }

  console.log(`操作系统: ${os.type()} ${os.release()}`);
  console.log(`Node 版本: ${process.version}`);
  console.log();

  // 2. dist 路径
  log('blue', '📁 dist 路径');
  console.log('-'.repeat(40));

  const distPath = detectDistPath();
  if (distPath) {
    log('green', `✅ 找到: ${distPath}`);
    const files = fs.readdirSync(distPath).filter(f => f.endsWith('.js') && !f.endsWith('.map'));
    console.log(`   文件数: ${files.length}`);
  } else {
    log('red', '❌ 未找到 dist 目录');
    console.log('   请设置 OPENCLAW_DIST 环境变量');
  }
  console.log();

  // 3. 端点检查
  if (distPath) {
    log('blue', '🔗 端点配置检查');
    console.log('-'.repeat(40));

    const checks = checkEndpoints(distPath);

    // 中国区端点
    console.log('\n中国区端点:');
    for (const [pattern, info] of Object.entries(checks)) {
      if (!info.isGlobal) {
        const status = info.found ? `${colors.green}✅` : `${colors.red}❌`;
        console.log(`  ${status} ${info.desc}: ${info.count} 处${colors.reset}`);
      }
    }

    // 全球端点 (应该被替换)
    console.log('\n全球端点 (应该已被替换):');
    let hasGlobalEndpoints = false;
    for (const [pattern, info] of Object.entries(checks)) {
      if (info.isGlobal) {
        const status = info.found ? `${colors.yellow}⚠️` : `${colors.green}✅`;
        const note = info.found ? `(${info.count} 处未替换)` : '(已全部替换)';
        console.log(`  ${status} ${info.desc}: ${note}${colors.reset}`);
        if (info.found) hasGlobalEndpoints = true;
      }
    }
    console.log();

    // 4. 诊断结论
    log('blue', '📋 诊断结论');
    console.log('-'.repeat(40));

    const chinaEndpointsConfigured = checks['login.chinacloudapi.cn'].found &&
      checks['api.botframework.azure.cn'].found;

    if (chinaEndpointsConfigured && !hasGlobalEndpoints) {
      log('green', '✅ 状态良好: 中国区端点已正确配置');
    } else if (chinaEndpointsConfigured && hasGlobalEndpoints) {
      log('yellow', '⚠️ 需要修复: 部分全球端点未替换');
      console.log('\n建议操作:');
      console.log('  1. 运行: node scripts/apply_patch.js');
      console.log('  2. 重启: openclaw gateway restart');
    } else {
      log('red', '❌ 需要修复: 中国区端点未配置');
      console.log('\n建议操作:');
      console.log('  1. 运行: node scripts/apply_patch.js');
      console.log('  2. 重启: openclaw gateway restart');
    }
  }

  console.log();
  console.log('='.repeat(60));
}

// 导出
module.exports = { diagnose, detectDistPath, checkEndpoints };

// 执行
if (require.main === module) {
  diagnose();
}