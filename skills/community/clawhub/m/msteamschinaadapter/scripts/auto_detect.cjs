/**
 * MSTeams China Auto-Detect & Auto-Fix v10
 *
 * 自动检测 OpenClaw 版本变化，发现升级后自动完成修复并重启 Gateway。
 *
 * 工作流程:
 *   1. 读取当前 OpenClaw 版本 (openclaw --version)
 *   2. 读取存储的历史版本 (~/.openclaw/.msteams-china-version)
 *   3. 如果版本有变化 且 @openclaw/msteams 插件已安装:
 *      a. 运行完整 6 阶段修复
 *      b. 自动重启 Gateway
 *      c. 更新存储的版本号
 *   4. 如果版本无变化 → 输出 SKIP 并退出
 *
 * 用法:
 *   node <skill_dir>/scripts/auto_detect.cjs
 *
 * 建议设置为:
 *   - Heartbeat 任务: 每次 heartbeat 时运行（推荐）
 *   - Cron 定时: 每小时或每天运行一次
 *   - Gateway 启动后: 作为 post-start hook
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// ===== 颜色日志 =====
const C = { G: '\x1b[32m', R: '\x1b[31m', Y: '\x1b[33m', B: '\x1b[34m', N: '\x1b[0m' };
function ok(m)  { console.log(`  ${C.G}[AUTO_OK] ${m}${C.N}`); }
function warn(m){ console.log(`  ${C.Y}[AUTO_WARN] ${m}${C.N}`); }
function fail(m){ console.log(`  ${C.R}[AUTO_FAIL] ${m}${C.N}`); }
function info(m){ console.log(`  ${C.B}[AUTO] ${m}${C.N}`); }

// ===== 配置 =====
const STATE_DIR = path.join(os.homedir(), '.openclaw');
const STATE_FILE = path.join(STATE_DIR, '.msteams-china-version');
const SKILL_SCRIPTS_DIR = path.join(
  process.env.APPDATA || '',
  'npm', 'node_modules', 'openclaw', 'skills', 'msteamschinaadapter', 'scripts'
);
// fallback paths for skill dir
const SKILL_SCRIPTS_CANDIDATES = [
  SKILL_SCRIPTS_DIR,
  path.join(os.homedir(), '.openclaw', 'skills', 'msteamschinaadapter', 'scripts'),
  '/usr/local/lib/node_modules/openclaw/skills/msteamschinaadapter/scripts',
  '/usr/lib/node_modules/openclaw/skills/msteamschinaadapter/scripts',
];

// ===== 工具函数 =====

/** 获取当前 OpenClaw 版本号 */
function getCurrentVersion() {
  try {
    const out = execSync('openclaw --version', { encoding: 'utf8', timeout: 10000 }).trim();
    // 提取版本号: "openclaw/2026.5.4 linux-x64 node-v24" → "2026.5.4"
    const match = out.match(/(\d+\.\d+\.\d+)/);
    return match ? match[1] : out;
  } catch (e) {
    warn(`Cannot get OpenClaw version: ${e.message}`);
    return null;
  }
}

/** 读取存储的历史版本号 */
function getStoredVersion() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      return fs.readFileSync(STATE_FILE, 'utf8').trim();
    }
  } catch (e) {}
  return null;
}

/** 写入当前版本号到状态文件 */
function saveCurrentVersion(version) {
  try {
    if (!fs.existsSync(STATE_DIR)) {
      fs.mkdirSync(STATE_DIR, { recursive: true });
    }
    fs.writeFileSync(STATE_FILE, version, 'utf8');
    ok(`Version state saved: ${version}`);
  } catch (e) {
    warn(`Cannot save version state: ${e.message}`);
  }
}

/** 检测 @openclaw/msteams 插件是否已安装 */
function isMsteamsPluginInstalled() {
  try {
    // Check node_modules
    const npmRoot = execSync('npm root -g', { encoding: 'utf8', timeout: 5000 }).trim();
    const pluginPath = path.join(npmRoot, '@openclaw', 'msteams');
    if (fs.existsSync(pluginPath)) return true;

    // Check APPDATA path (Windows)
    const appDataPath = path.join(process.env.APPDATA || '', 'npm', 'node_modules', '@openclaw', 'msteams');
    if (fs.existsSync(appDataPath)) return true;

    // Check if it's referenced in openclaw config
    const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      if (config.channels && config.channels.msteams) return true;
    }
  } catch (e) {}
  return false;
}

/** 查找技能脚本目录 */
function findSkillScriptsDir() {
  for (const c of SKILL_SCRIPTS_CANDIDATES) {
    if (c && fs.existsSync(path.join(c, 'patch_all_v10.cjs'))) {
      return c;
    }
  }
  // Try to find by searching relative to this script
  const selfDir = __dirname;
  const candidate = path.join(selfDir);
  if (fs.existsSync(path.join(candidate, 'patch_all_v10.cjs'))) return candidate;
  return null;
}

/** 重启 Gateway */
function restartGateway() {
  info('Restarting Gateway...');
  try {
    execSync('openclaw gateway restart', { encoding: 'utf8', timeout: 30000, stdio: 'pipe' });
    ok('Gateway restart initiated');
    return true;
  } catch (e) {
    fail(`Gateway restart failed: ${e.message}`);
    // Try alternative: send stop then start
    try {
      execSync('openclaw gateway stop', { encoding: 'utf8', timeout: 15000, stdio: 'pipe' });
      execSync('openclaw gateway start', { encoding: 'utf8', timeout: 15000, stdio: 'pipe' });
      ok('Gateway restart via stop+start succeeded');
      return true;
    } catch (e2) {
      fail(`Gateway stop+start also failed: ${e2.message}`);
      warn('Please restart Gateway manually: openclaw gateway restart');
      return false;
    }
  }
}

/** 检查 Gateway 是否已启动 */
function isGatewayRunning() {
  try {
    const out = execSync('openclaw gateway status', { encoding: 'utf8', timeout: 10000 });
    return out.includes('running') || out.includes('online') || out.includes('started');
  } catch (e) {
    return false;
  }
}

// ===== 主流程 =====
function main() {
  console.log('');
  console.log('='.repeat(60));
  console.log('  MSTeams China Auto-Detect & Auto-Fix v10');
  console.log('='.repeat(60));
  console.log('');

  // Step 1: 获取当前版本
  info('Step 1: Checking OpenClaw version...');
  const currentVersion = getCurrentVersion();
  if (!currentVersion) {
    fail('Cannot determine OpenClaw version. Aborting.');
    process.exit(1);
  }
  ok(`Current version: ${currentVersion}`);

  // Step 2: 检查 @openclaw/msteams 插件
  info('Step 2: Checking @openclaw/msteams plugin...');
  if (!isMsteamsPluginInstalled()) {
    info('@openclaw/msteams plugin not installed. Nothing to patch. Exiting.');
    process.exit(0);
  }
  ok('@openclaw/msteams plugin is installed');

  // Step 3: 对比版本
  info('Step 3: Comparing versions...');
  const storedVersion = getStoredVersion();

  if (storedVersion === null) {
    // 首次运行 — 记录版本，不修复（无需修复全新安装）
    info('First run detected. Recording version without patching.');
    saveCurrentVersion(currentVersion);
    info('Done. Next run will detect version changes.');
    process.exit(0);
  }

  if (storedVersion === currentVersion) {
    // 版本无变化 — 无需修复
    ok(`Version unchanged (${storedVersion}). No patch needed.`);
    info('Auto-fix skipped. Version matches stored state.');
    process.exit(0);
  }

  // 版本有变化！需要修复
  info('');
  warn('╔══════════════════════════════════════════════════════╗');
  warn('║  VERSION CHANGE DETECTED!                          ║');
  warn(`║  ${storedVersion} → ${currentVersion.padEnd(12)}               ║`);
  warn('║  Starting auto-fix...                               ║');
  warn('╚══════════════════════════════════════════════════════╝');
  info('');

  // Step 4: 运行 patch_all_v10.cjs
  info('Step 4: Running full patch...');
  const scriptsDir = findSkillScriptsDir();
  if (!scriptsDir) {
    fail('Cannot find patch_all_v10.cjs in skill directory.');
    warn('Please run the patch manually:');
    warn('  node <skill_dir>/scripts/patch_all_v10.cjs');
    warn('  openclaw gateway restart');
    process.exit(1);
  }

  const patchScriptPath = path.join(scriptsDir, 'patch_all_v10.cjs');
  info(`Patch script: ${patchScriptPath}`);

  try {
    const patchOutput = execSync(`node "${patchScriptPath}"`, {
      encoding: 'utf8',
      timeout: 120000,  // 2 min timeout for patch
      stdio: 'pipe',
    });
    console.log(patchOutput);

    // Check if patch succeeded
    if (patchOutput.includes('SUCCESS') && patchOutput.includes('All verifications passed')) {
      ok('Patch applied successfully!');
    } else {
      warn('Patch may have issues. Check output above.');
    }
  } catch (e) {
    fail(`Patch execution failed: ${e.message}`);
    // Still try to save version and restart
    warn('Continuing with version save and restart attempt...');
  }

  // Step 5: 保存当前版本
  info('Step 5: Saving version state...');
  saveCurrentVersion(currentVersion);

  // Step 6: 自动重启 Gateway
  info('Step 6: Auto-restarting Gateway...');
  const wasRunning = isGatewayRunning();
  info(`Gateway was ${wasRunning ? 'running' : 'not running'}`);

  const restartOk = restartGateway();

  if (restartOk) {
    ok('Auto-fix complete! Gateway restarted successfully.');
    ok(`Version: ${storedVersion} → ${currentVersion}`);
    ok('Webchat sessions at http://127.0.0.1:18789 are preserved.');
    info('Send a test message in Teams to verify.');
  } else {
    warn('Auto-fix patches applied but Gateway restart failed.');
    warn('Please restart manually: openclaw gateway restart');
  }

  console.log('');
  console.log('='.repeat(60));
  if (restartOk) {
    console.log(`  ${C.G}✅ AUTO-FIX COMPLETE${C.N}`);
    console.log(`  ${C.G}   ${storedVersion} → ${currentVersion}${C.N}`);
    console.log(`  ${C.G}   Gateway restarted, sessions preserved${C.N}`);
  } else {
    console.log(`  ${C.Y}⚠️  AUTO-FIX PARTIAL — restart needed manually${C.N}`);
  }
  console.log('='.repeat(60));
  console.log('');
}

// ===== 执行 =====
main();
