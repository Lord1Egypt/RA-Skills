/**
 * OpenClaw MS Teams China Adapter Patch v10 — 中国区全自动修复脚本
 *
 * 修复内容:
 *   Phase 1: OpenClaw 核心 dist 端点补丁
 *   Phase 2: MSTeams 插件 dist 端点补丁（graph-users/oauth.token/BotFramework JWT/MSAL/SSRF）
 *   Phase 3: 注入 cloud: sdk.CHINA 到 App 构造函数
 *   Phase 4: 注入 cloud: sdk.CHINA 到 Federated/Token App 构造函数
 *   Phase 5: 设置系统级环境变量 (CLOUD, SERVICE_URL)
 *   Phase 6: 验证所有补丁
 *
 * 用法: node patch_all.cjs
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// ===== 日志工具 =====
const C = { G: '\x1b[32m', R: '\x1b[31m', Y: '\x1b[33m', B: '\x1b[34m', N: '\x1b[0m' };
function ok(m) { console.log(`  ${C.G}[OK] ${m}${C.N}`); }
function warn(m) { console.log(`  ${C.Y}[WARN] ${m}${C.N}`); }
function fail(m) { console.log(`  ${C.R}[FAIL] ${m}${C.N}`); }
function info(m) { console.log(`  ${C.B}[INFO] ${m}${C.N}`); }
function heading(m) { console.log(`\n${C.B}${m}${C.N}`); console.log('-'.repeat(40)); }

// ===== 路径检测 =====
function detectDistPath() {
  const candidates = [
    path.join(process.env.APPDATA || '', 'npm', 'node_modules', 'openclaw', 'dist'),
    path.join(process.cwd(), 'node_modules', 'openclaw', 'dist'),
    path.join(os.homedir(), '.nvm', 'versions', 'node', process.version, 'lib', 'node_modules', 'openclaw', 'dist'),
    '/usr/local/lib/node_modules/openclaw/dist',
    '/usr/lib/node_modules/openclaw/dist',
    process.env.OPENCLAW_DIST,
  ].filter(Boolean);
  for (const c of candidates) { if (c && fs.existsSync(c)) return c; }
  try {
    const npmRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    const dp = path.join(npmRoot, 'openclaw', 'dist');
    if (fs.existsSync(dp)) return dp;
  } catch (e) {}
  return null;
}

function detectPluginDistPath() {
  const candidates = [
    path.join(process.env.APPDATA || '', 'npm', 'node_modules', '@openclaw', 'msteams', 'dist'),
    path.join(os.homedir(), '.openclaw', 'npm', 'node_modules', '@openclaw', 'msteams', 'dist'),
    path.join(process.cwd(), 'node_modules', '@openclaw', 'msteams', 'dist'),
    '/usr/local/lib/node_modules/@openclaw/msteams/dist',
    '/usr/lib/node_modules/@openclaw/msteams/dist',
  ].filter(Boolean);
  for (const c of candidates) { if (c && fs.existsSync(c)) return c; }
  try {
    const npmRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    const dp = path.join(npmRoot, '@openclaw', 'msteams', 'dist');
    if (fs.existsSync(dp)) return dp;
  } catch (e) {}
  return null;
}

console.log('='.repeat(60));
console.log('OpenClaw MS Teams China Patch v10');
console.log('='.repeat(60));

const DIST = detectDistPath();
const PLUGIN_DIST = detectPluginDistPath();

if (!DIST) { fail('OpenClaw core dist not found!'); process.exit(1); }
if (!PLUGIN_DIST) { fail('MSTeams plugin dist not found!'); process.exit(1); }

info(`OpenClaw dist: ${DIST}`);
info(`Plugin dist:   ${PLUGIN_DIST}`);

// ===== Phase 1: OpenClaw 核心 dist 端点补丁 (来自 v9) =====
heading('Phase 1: OpenClaw core dist endpoint patches');
const coreFiles = fs.readdirSync(DIST).filter(f => f.endsWith('.js') && !f.endsWith('.map'));
info(`${coreFiles.length} files indexed`);

function readCore(fn) { return fs.readFileSync(path.join(DIST, fn), 'utf8'); }
function writeCore(fn, c) { fs.writeFileSync(path.join(DIST, fn), c); }

function locateCore(markers) {
  for (const f of coreFiles) {
    const c = readCore(f);
    if (markers.every(m => c.includes(m))) return { file: f, content: c };
  }
  return null;
}

const replacements = [
  { from: 'DEFAULT_AUTHORITY: "https://login.microsoftonline.com/common/"', to: 'DEFAULT_AUTHORITY: "https://login.chinacloudapi.cn/common/"' },
  { from: 'DEFAULT_AUTHORITY_HOST: "login.microsoftonline.com"', to: 'DEFAULT_AUTHORITY_HOST: "login.chinacloudapi.cn"' },
  { from: 'AAD_INSTANCE_DISCOVERY_ENDPT: "https://login.microsoftonline.com/common/discovery/instance?api-version=1.1&authorization_endpoint="', to: 'AAD_INSTANCE_DISCOVERY_ENDPT: "https://login.chinacloudapi.cn/common/discovery/instance?api-version=1.1&authorization_endpoint="' },
  { from: 'AzurePublic: "https://login.microsoftonline.com"', to: 'AzurePublic: "https://login.chinacloudapi.cn"' },
  { from: 'const DEFAULT_API_CLIENT_SETTINGS = { oauthUrl: "https://token.botframework.com" };', to: 'const DEFAULT_API_CLIENT_SETTINGS = { oauthUrl: "https://token.botframework.azure.cn" };' },
];

let p1 = 0;
for (const r of replacements) {
  const parts = r.from.split(':');
  const marker = parts[0].replace('const ', '').trim();
  const located = locateCore([marker]);
  if (!located) { warn(`Marker '${marker}' not found in core dist`); continue; }
  let content = readCore(located.file);
  if (content.includes(r.to)) { continue; }
  if (content.includes(r.from)) {
    content = content.replace(r.from, r.to);
    writeCore(located.file, content);
    ok(`Core: ${marker}`);
    p1++;
  }
}
info(`Phase 1 result: ${p1} patched`);

// ===== Phase 2: 全局字符串替换 (OpenClaw core dist) =====
heading('Phase 2: Global replacements in core dist');
const globalRepl = [
  ['https://login.microsoftonline.com/common/discovery/v2.0/keys', 'https://login.chinacloudapi.cn/common/discovery/v2.0/keys'],
  ['DEFAULT_AUTHORITY: "https://login.microsoftonline.com/common/"', 'DEFAULT_AUTHORITY: "https://login.chinacloudapi.cn/common/"'],
];
let p2 = 0;
for (const [from, to] of globalRepl) {
  for (const f of coreFiles) {
    let c = readCore(f);
    if (c.includes(to)) continue;
    if (c.includes(from)) { c = c.split(from).join(to); writeCore(f, c); p2++; }
  }
}
info(`Phase 2 result: ${p2} replacements`);

// ===== Phase 3: Patch MSTeams plugin dist =====
heading('Phase 3: MSTeams plugin dist patches');
const pluginFiles = fs.readdirSync(PLUGIN_DIST).filter(f => f.endsWith('.js') && !f.endsWith('.map'));
function readPlugin(fn) { return fs.readFileSync(path.join(PLUGIN_DIST, fn), 'utf8'); }
function writePlugin(fn, c) { fs.writeFileSync(path.join(PLUGIN_DIST, fn), c); }

const graphFile = pluginFiles.find(f => f.startsWith('graph-users-'));
const oauthFile = pluginFiles.find(f => f.startsWith('oauth.token-'));

if (!graphFile) { fail('graph-users-*.js not found in plugin dist!'); process.exit(1); }
if (!oauthFile) { fail('oauth.token-*.js not found in plugin dist!'); process.exit(1); }

let graphContent = readPlugin(graphFile);
let p3 = 0;

// 3a. GRAPH_ROOT
if (!graphContent.includes('https://microsoftgraph.chinacloudapi.cn/v1.0')) {
  graphContent = graphContent.replace(
    'const GRAPH_ROOT = "https://graph.microsoft.com/v1.0";',
    'const GRAPH_ROOT = "https://microsoftgraph.chinacloudapi.cn/v1.0";'
  );
  ok('GRAPH_ROOT'); p3++;
}

// 3b. DEFAULT_MEDIA_HOST_ALLOWLIST - add microsoftgraph.chinacloudapi.cn
if (!graphContent.includes('"microsoftgraph.chinacloudapi.cn"') || !graphContent.includes('DEFAULT_MEDIA_HOST_ALLOWLIST')) {
  graphContent = graphContent.replace(
    '"sharepoint.com",',
    '"microsoftgraph.chinacloudapi.cn",\n\t"sharepoint.com",'
  );
  ok('DEFAULT_MEDIA_HOST_ALLOWLIST'); p3++;
}

// 3c. DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST - fix botframework.com + add microsoftgraph
if (graphContent.includes('"api.botframework.com"')) {
  graphContent = graphContent.replace('"api.botframework.com",', '"api.botframework.azure.cn",');
  ok('DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST (botframework)'); p3++;
}
if (!graphContent.includes('"microsoftgraph.chinacloudapi.cn"') || !graphContent.includes('DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST')) {
  graphContent = graphContent.replace(
    'const DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST = [',
    'const DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST = [\n\t"microsoftgraph.chinacloudapi.cn",'
  );
  ok('DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST (microsoftgraph)'); p3++;
}

// 3d. BOT_FRAMEWORK_GLOBAL_AUDIENCE
if (graphContent.includes('"https://api.botframework.com"')) {
  graphContent = graphContent.replace(
    'const BOT_FRAMEWORK_GLOBAL_AUDIENCE = "https://api.botframework.com";',
    'const BOT_FRAMEWORK_GLOBAL_AUDIENCE = "https://api.botframework.azure.cn";'
  );
  ok('BOT_FRAMEWORK_GLOBAL_AUDIENCE'); p3++;
}

// 3e. BOT_FRAMEWORK_ISSUERS - botframework.com -> azure.cn
if (graphContent.includes('issuer: "https://api.botframework.com"')) {
  graphContent = graphContent.replace('issuer: "https://api.botframework.com"', 'issuer: "https://api.botframework.azure.cn"');
  graphContent = graphContent.replace('jwksUri: "https://login.botframework.com/v1/.well-known/keys"', 'jwksUri: "https://login.botframework.azure.cn/v1/.well-known/keys"');
  ok('BOT_FRAMEWORK_ISSUERS'); p3++;
}

// 3f. MSAL login.microsoftonline.com -> chinacloudapi.cn (for Entra issuers)
if (graphContent.includes('https://login.microsoftonline.com/')) {
  graphContent = graphContent.replaceAll('https://login.microsoftonline.com/', 'https://login.chinacloudapi.cn/');
  ok('MSAL login endpoints'); p3++;
}

// 3g. STS issuer
if (graphContent.includes('sts.windows.net')) {
  graphContent = graphContent.replaceAll('sts.windows.net', 'sts.chinacloudapi.cn');
  ok('STS issuers'); p3++;
}

writePlugin(graphFile, graphContent);
info(`Phase 3 result: ${p3} plugin patches`);

// ===== Phase 4: Patch OAuth token endpoints =====
heading('Phase 4: OAuth token endpoints');
let oauthContent = readPlugin(oauthFile);
let p4 = 0;

if (oauthContent.includes('https://login.microsoftonline.com/')) {
  oauthContent = oauthContent.replaceAll('https://login.microsoftonline.com/', 'https://login.chinacloudapi.cn/');
  writePlugin(oauthFile, oauthContent);
  ok('OAuth token endpoints'); p4++;
}
info(`Phase 4 result: ${p4} patches`);

// ===== Phase 5: Inject cloud: sdk.CHINA into App constructors =====
heading('Phase 5: SDK cloud: CHINA injection');
graphContent = readPlugin(graphFile);
let p5 = 0;

// 5a. Secret auth App constructor
const secPattern = 'return new sdk.App({\n\t\tclientId: creds.appId,\n\t\tclientSecret: creds.appPassword,\n\t\ttenantId: creds.tenantId,\n\t\thttpServerAdapter: createNoOpHttpServerAdapter()\n\t});';
const secFixed = 'return new sdk.App({\n\t\tclientId: creds.appId,\n\t\tclientSecret: creds.appPassword,\n\t\ttenantId: creds.tenantId,\n\t\tcloud: sdk.CHINA,\n\t\thttpServerAdapter: createNoOpHttpServerAdapter()\n\t});';

if (graphContent.includes('cloud: sdk.CHINA')) {
  ok('cloud: sdk.CHINA already injected (secret)');
} else if (graphContent.includes(secPattern)) {
  graphContent = graphContent.replace(secPattern, secFixed);
  ok('cloud: sdk.CHINA injected (secret auth)'); p5++;
} else {
  // Try simpler pattern
  const altSec = 'clientId: creds.appId,\n\t\tclientSecret: creds.appPassword,\n\t\ttenantId: creds.tenantId,\n\t\thttpServerAdapter: createNoOpHttpServerAdapter()';
  const altFixed = 'clientId: creds.appId,\n\t\tclientSecret: creds.appPassword,\n\t\ttenantId: creds.tenantId,\n\t\tcloud: sdk.CHINA,\n\t\thttpServerAdapter: createNoOpHttpServerAdapter()';
  if (graphContent.includes(altSec)) {
    graphContent = graphContent.replace(altSec, altFixed);
    ok('cloud: sdk.CHINA injected (secret auth, alt pattern)'); p5++;
  } else {
    warn('Secret auth App constructor pattern not found');
  }
}

// 5b. Federated/Token auth App constructor
const fedPattern = 'return new sdk.App({\n\t\tclientId: creds.appId,\n\t\ttenantId: creds.tenantId,\n\t\ttoken: tokenProvider,\n\t\thttpServerAdapter: createNoOpHttpServerAdapter()\n\t});';
const fedFixed = 'return new sdk.App({\n\t\tclientId: creds.appId,\n\t\ttenantId: creds.tenantId,\n\t\tcloud: sdk.CHINA,\n\t\ttoken: tokenProvider,\n\t\thttpServerAdapter: createNoOpHttpServerAdapter()\n\t});';

if (graphContent.includes(fedPattern)) {
  graphContent = graphContent.replace(fedPattern, fedFixed);
  ok('cloud: sdk.CHINA injected (federated/token auth)'); p5++;
} else {
  const altFed = 'tenantId: creds.tenantId,\n\t\ttoken: tokenProvider,\n\t\thttpServerAdapter: createNoOpHttpServerAdapter()';
  const altFedFixed = 'tenantId: creds.tenantId,\n\t\tcloud: sdk.CHINA,\n\t\ttoken: tokenProvider,\n\t\thttpServerAdapter: createNoOpHttpServerAdapter()';
  if (graphContent.includes(altFed)) {
    graphContent = graphContent.replace(altFed, altFedFixed);
    ok('cloud: sdk.CHINA injected (federated/token, alt pattern)'); p5++;
  } else {
    warn('Federated auth App constructor pattern not found');
  }
}

if (p5 > 0) writePlugin(graphFile, graphContent);
info(`Phase 5 result: ${p5} cloud injections`);

// ===== Phase 6: Set environment variables =====
heading('Phase 6: Environment variables');

let p6 = 0;
try {
  const curCloud = process.env.CLOUD || execSync('reg query HKCU\\Environment /v CLOUD 2>nul', { encoding: 'utf8' }).trim() || '';
  const curServiceUrl = process.env.SERVICE_URL || '';

  if (curCloud.toLowerCase() !== 'china') {
    const isWin = os.platform() === 'win32';
    if (isWin) {
      execSync('reg add HKCU\\Environment /v CLOUD /t REG_SZ /d china /f', { stdio: 'pipe' });
      execSync('reg add HKCU\\Environment /v SERVICE_URL /t REG_SZ /d "https://smba.trafficmanager.cn/teams" /f', { stdio: 'pipe' });
      // Also try system level
      try { execSync('reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment /v CLOUD /t REG_SZ /d china /f', { stdio: 'pipe' }); } catch(e) {}
      try { execSync('reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment /v SERVICE_URL /t REG_SZ /d "https://smba.trafficmanager.cn/teams" /f', { stdio: 'pipe' }); } catch(e) {}
    } else {
      execSync('echo "export CLOUD=china" >> ~/.bashrc', { stdio: 'pipe' });
      execSync('echo "export SERVICE_URL=https://smba.trafficmanager.cn/teams" >> ~/.bashrc', { stdio: 'pipe' });
    }
    ok('CLOUD=china and SERVICE_URL set'); p6++;
  } else {
    ok('CLOUD=china already set');
  }
} catch (e) {
  warn(`Could not set environment variables: ${e.message}`);
  warn('Please set manually: CLOUD=china, SERVICE_URL=https://smba.trafficmanager.cn/teams');
}
info(`Phase 6 result: ${p6} env vars set`);

// ===== Phase 7: Verification =====
heading('Phase 7: Verification');
let allPass = true;

// Read updated files
graphContent = readPlugin(graphFile);
oauthContent = readPlugin(oauthFile);

const verifyChecks = [
  { name: 'Plugin GRAPH_ROOT', pattern: 'https://microsoftgraph.chinacloudapi.cn/v1.0', content: graphContent },
  { name: 'Plugin Allowlist (microsoftgraph)', pattern: '"microsoftgraph.chinacloudapi.cn"', content: graphContent },
  { name: 'Plugin Bot Framework China', pattern: 'https://api.botframework.azure.cn', content: graphContent },
  { name: 'Plugin MSAL China', pattern: 'https://login.chinacloudapi.cn/', content: graphContent },
  { name: 'Plugin STS China', pattern: 'sts.chinacloudapi.cn', content: graphContent },
  { name: 'Plugin OAuth China', pattern: 'https://login.chinacloudapi.cn/', content: oauthContent },
  { name: 'Plugin cloud: sdk.CHINA (secret)', pattern: 'cloud: sdk.CHINA', content: graphContent },
  { name: 'Plugin BOT_FRAMEWORK_GLOBAL_AUDIENCE China', pattern: 'https://api.botframework.azure.cn', content: graphContent },
];

// Core dist checks
for (const f of coreFiles) {
  const c = readCore(f);
  verifyChecks.push(
    { name: `Core login.chinacloudapi.cn in ${f.substring(0, 20)}`, pattern: 'login.chinacloudapi.cn', content: c },
  );
  break; // Just check first file
}

for (const check of verifyChecks) {
  if (check.content.includes(check.pattern)) {
    ok(check.name);
  } else {
    fail(`${check.name} — missing "${check.pattern}"`);
    allPass = false;
  }
}

// ===== Final =====
console.log('\n' + '='.repeat(60));
const total = p1 + p2 + p3 + p4 + p5 + p6;
if (allPass) {
  console.log(`${C.G}SUCCESS: ${total} patches applied. All verifications passed.${C.N}`);
  console.log(`  Phase 1-2 (Core dist):  ${p1 + p2} patches`);
  console.log(`  Phase 3-4 (Plugin dist): ${p3 + p4} patches`);
  console.log(`  Phase 5 (SDK cloud):     ${p5} injections`);
  console.log(`  Phase 6 (Env vars):      ${p6} set`);
  console.log(`\nIMPORTANT: You MUST restart the gateway:`);
  console.log(`  openclaw gateway restart`);
  console.log(`\nAfter restart, verify by sending a message to the Teams bot.`);
} else {
  console.log(`${C.R}FAIL: Some verifications failed. Check the [FAIL] items above.${C.N}`);
  process.exit(1);
}
console.log('='.repeat(60));
