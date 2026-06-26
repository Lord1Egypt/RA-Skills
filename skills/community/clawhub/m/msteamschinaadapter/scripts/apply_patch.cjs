/**
 * OpenClaw MS Teams China Adapter Patch Script v9
 *
 * 自动修补 OpenClaw msteams 扩展，支持 Microsoft Teams 中国区 (世纪互联/21Vianet)
 *
 * 特性:
 * - 跨平台自动检测 dist 路径 (Windows/macOS/Linux)
 * - 四阶段修复：Marker 补丁 + 全局替换 + SSRF Allowlist + 验证
 * - SSRF Allowlist: 自动添加 microsoftgraph.chinacloudapi.cn 到媒体允许列表
 * - 热修复友好：先应用所有补丁，最后提示重启
 * - 幂等：已打补丁自动跳过
 * - 详细日志：输出修复统计和验证结果
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// ===== 跨平台 dist 路径检测 =====
function detectDistPath() {
  const candidates = [
    // Windows - npm global
    path.join(process.env.APPDATA || '', 'npm', 'node_modules', 'openclaw', 'dist'),
    // Windows - local node_modules
    path.join(process.cwd(), 'node_modules', 'openclaw', 'dist'),
    // macOS/Linux - nvm
    path.join(os.homedir(), '.nvm', 'versions', 'node', process.version, 'lib', 'node_modules', 'openclaw', 'dist'),
    // macOS/Linux - npm global
    '/usr/local/lib/node_modules/openclaw/dist',
    '/usr/lib/node_modules/openclaw/dist',
    // Custom via environment variable
    process.env.OPENCLAW_DIST,
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (candidate && fs.existsSync(candidate)) {
      return candidate;
    }
  }

  // Fallback: try to find via npm root
  try {
    const { execSync } = require('child_process');
    const npmRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    const distPath = path.join(npmRoot, 'openclaw', 'dist');
    if (fs.existsSync(distPath)) return distPath;
  } catch (e) { /* ignore */ }

  throw new Error('Cannot find OpenClaw dist directory. Set OPENCLAW_DIST environment variable.');
}

const OPENCLAW_DIST = detectDistPath();

console.log('='.repeat(60));
console.log('OpenClaw MS Teams China Patch v9');
console.log('='.repeat(60));
console.log(`Dist: ${OPENCLAW_DIST}\n`);

// ===== 构建文件索引 =====
console.log('Indexing dist files...');
const fileList = [];
for (const file of fs.readdirSync(OPENCLAW_DIST).filter(f => f.endsWith('.js') && !f.endsWith('.map'))) {
  fileList.push(file);
}
console.log(`  ${fileList.length} files indexed\n`);

// ===== 辅助函数 =====
function readFileContent(filename) {
  return fs.readFileSync(path.join(OPENCLAW_DIST, filename), 'utf8');
}

function writeFileContent(filename, content) {
  fs.writeFileSync(path.join(OPENCLAW_DIST, filename), content);
}

function locateFile(markers) {
  for (const file of fileList) {
    const content = readFileContent(file);
    if (markers.every(m => content.includes(m))) {
      return { file, content };
    }
  }
  return null;
}

// ===== 第一阶段：Marker 补丁 =====
console.log('Phase 1: Marker-based patches');
console.log('-'.repeat(40));

const markerPatches = [
  // === MSAL 核心配置 ===
  {
    name: 'MSAL DEFAULT_AUTHORITY',
    markers: ['DEFAULT_AUTHORITY:', 'login.microsoftonline.com/common/'],
    patterns: [
      { old: 'DEFAULT_AUTHORITY: "https://login.microsoftonline.com/common/"', new: 'DEFAULT_AUTHORITY: "https://login.chinacloudapi.cn/common/"' }
    ]
  },
  {
    name: 'MSAL DEFAULT_AUTHORITY_HOST',
    markers: ['DEFAULT_AUTHORITY_HOST:', 'login.microsoftonline.com'],
    patterns: [
      { old: 'DEFAULT_AUTHORITY_HOST: "login.microsoftonline.com"', new: 'DEFAULT_AUTHORITY_HOST: "login.chinacloudapi.cn"' }
    ]
  },
  {
    name: 'MSAL AAD_INSTANCE_DISCOVERY_ENDPT',
    markers: ['AAD_INSTANCE_DISCOVERY_ENDPT:', 'login.microsoftonline.com/common/discovery'],
    patterns: [
      { old: 'AAD_INSTANCE_DISCOVERY_ENDPT: "https://login.microsoftonline.com/common/discovery/instance?api-version=1.1&authorization_endpoint="', new: 'AAD_INSTANCE_DISCOVERY_ENDPT: "https://login.chinacloudapi.cn/common/discovery/instance?api-version=1.1&authorization_endpoint="' }
    ]
  },
  {
    name: 'GET_DEFAULT_TOKEN_AUTHORITY',
    markers: ['GET_DEFAULT_TOKEN_AUTHORITY', 'login.microsoftonline.com'],
    patterns: [
      { old: 'const GET_DEFAULT_TOKEN_AUTHORITY = (tenantId) => `https://login.microsoftonline.com/${tenantId}`;', new: 'const GET_DEFAULT_TOKEN_AUTHORITY = (tenantId) => `https://login.chinacloudapi.cn/${tenantId}`;' }
    ]
  },
  {
    name: 'MSAL AzurePublic',
    markers: ['AzurePublic:', 'login.microsoftonline.com'],
    patterns: [
      { old: 'AzurePublic: "https://login.microsoftonline.com"', new: 'AzurePublic: "https://login.chinacloudapi.cn"' }
    ]
  },

  // === Bot Framework 端点 ===
  {
    name: 'DEFAULT_BOT_TOKEN_SCOPE',
    markers: ['DEFAULT_BOT_TOKEN_SCOPE', 'api.botframework.com'],
    patterns: [
      { old: 'const DEFAULT_BOT_TOKEN_SCOPE = "https://api.botframework.com/.default";', new: 'const DEFAULT_BOT_TOKEN_SCOPE = "https://api.botframework.azure.cn/.default";' }
    ]
  },
  {
    name: 'API Client oauthUrl',
    markers: ['DEFAULT_API_CLIENT_SETTINGS', 'token.botframework'],
    patterns: [
      { old: 'const DEFAULT_API_CLIENT_SETTINGS = { oauthUrl: "https://token.botframework.com" };', new: 'const DEFAULT_API_CLIENT_SETTINGS = { oauthUrl: "https://token.botframework.azure.cn" };' }
    ]
  },

  // === Graph API ===
  {
    name: 'GRAPH_ROOT',
    markers: ['GRAPH_ROOT', 'graph.microsoft.com/v1.0'],
    patterns: [
      { old: 'const GRAPH_ROOT = "https://graph.microsoft.com/v1.0";', new: 'const GRAPH_ROOT = "https://microsoftgraph.chinacloudapi.cn/v1.0";' }
    ]
  },

  // === JWT Validator ===
  {
    name: 'JWT Validator JWKS URI',
    markers: ['login.botframework.com/v1/.well-known/keys'],
    patterns: [
      { old: 'uri: "https://login.botframework.com/v1/.well-known/keys"', new: 'uri: "https://login.botframework.azure.cn/v1/.well-known/keys"' }
    ]
  },
  {
    name: 'JWT Validator allowedIssuer',
    markers: ['allowedIssuer:', 'api.botframework.com'],
    patterns: [
      { old: 'validateIssuer: { allowedIssuer: "https://api.botframework.com" }', new: 'validateIssuer: { allowedIssuer: "https://api.botframework.azure.cn" }' }
    ]
  },

  // === scopeCandidatesForUrl ===
  {
    name: 'scopeCandidatesForUrl Graph domain',
    markers: ['scopeCandidatesForUrl', 'graph.microsoft.com'],
    patterns: [
      { old: 'host.endsWith("graph.microsoft.com") || host.endsWith("sharepoint.com")', new: 'host.endsWith("graph.microsoft.com") || host.endsWith("microsoftgraph.chinacloudapi.cn") || host.endsWith("sharepoint.com")' }
    ]
  },
];

const stats = { patched: 0, already: 0, missing: 0, not_found: 0 };

for (const patch of markerPatches) {
  const located = locateFile(patch.markers);
  if (!located) {
    console.log(`[WARN] ${patch.name} - file not found`);
    stats.not_found++;
    continue;
  }

  let content = readFileContent(located.file);
  let patched = false;
  let alreadyPatched = false;

  for (const pattern of patch.patterns) {
    if (content.includes(pattern.new)) {
      alreadyPatched = true;
    } else if (content.includes(pattern.old)) {
      content = content.replace(pattern.old, pattern.new);
      patched = true;
    }
  }

  if (patched) {
    writeFileContent(located.file, content);
    console.log(`[OK]   ${patch.name}`);
    stats.patched++;
  } else if (alreadyPatched) {
    stats.already++;
  } else {
    console.log(`[SKIP] ${patch.name} - pattern not found`);
    stats.missing++;
  }
}

console.log(`\nPhase 1 result: ${stats.patched} patched, ${stats.already} already, ${stats.missing} missing, ${stats.not_found} not found\n`);

// ===== 第二阶段：全局替换 =====
console.log('Phase 2: Global replacements');
console.log('-'.repeat(40));

const globalReplacements = [
  // Bot Framework 端点 (先替换具体的，再替换通用的)
  { from: 'https://login.botframework.com/v1/.well-known/keys', to: 'https://login.botframework.azure.cn/v1/.well-known/keys', desc: 'Bot Framework JWKS' },
  { from: '"https://api.botframework.com"', to: '"https://api.botframework.azure.cn"', desc: 'api.botframework.com -> azure.cn' },
  { from: '"api.botframework.com"', to: '"api.botframework.azure.cn"', desc: 'api.botframework.com (bare) -> azure.cn' },
  
  // Graph API 端点
  { from: 'getAccessToken("https://graph.microsoft.com")', to: 'getAccessToken("https://microsoftgraph.chinacloudapi.cn")', desc: 'Graph scope' },
  { from: 'https://login.microsoftonline.com/common/discovery/v2.0/keys', to: 'https://login.chinacloudapi.cn/common/discovery/v2.0/keys', desc: 'Discovery keys endpoint' },
  
  // MSAL issuer 验证
  { from: 'https://login.microsoftonline.com/${tenantId}', to: 'https://login.chinacloudapi.cn/${tenantId}', desc: 'Issuer template' },
];

const globalStats = { patched: 0, skipped: 0 };

for (const repl of globalReplacements) {
  let patchedFiles = 0;
  
  for (const file of fileList) {
    let content = readFileContent(file);
    
    if (content.includes(repl.to)) {
      // 已经替换过
      continue;
    }
    
    if (content.includes(repl.from)) {
      content = content.split(repl.from).join(repl.to);
      writeFileContent(file, content);
      patchedFiles++;
    }
  }
  
  if (patchedFiles > 0) {
    console.log(`[OK]   ${repl.desc} (${patchedFiles} files)`);
    globalStats.patched++;
  } else {
    globalStats.skipped++;
  }
}

console.log(`\nPhase 2 result: ${globalStats.patched} replacements made, ${globalStats.skipped} skipped\n`);

// ===== 第三阶段：SSRF Allowlist 补丁 =====
console.log('Phase 3: SSRF Allowlist patches');
console.log('-'.repeat(40));

const ssrfStats = { patched: 0, already: 0, not_found: 0 };

// SSRF Allowlist 补丁 - 修复 Graph API 请求被安全策略阻止的问题
// 关键文件: graph-users-*.js 包含 DEFAULT_MEDIA_HOST_ALLOWLIST 和 DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST
const ssrfPatches = [
  {
    name: 'DEFAULT_MEDIA_HOST_ALLOWLIST',
    markers: ['DEFAULT_MEDIA_HOST_ALLOWLIST', 'graph.microsoft.cn', 'sharepoint.cn'],
    addPattern: 'microsoftgraph.chinacloudapi.cn',
    desc: '添加中国区 Graph API 到媒体主机允许列表'
  },
  {
    name: 'DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST',
    markers: ['DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST', 'api.botframework.azure.cn', 'botframework.com'],
    addPattern: 'microsoftgraph.chinacloudapi.cn',
    desc: '添加中国区 Graph API 到认证主机允许列表'
  }
];

for (const patch of ssrfPatches) {
  const located = locateFile(patch.markers);
  if (!located) {
    console.log(`[WARN] ${patch.name} - file not found`);
    ssrfStats.not_found++;
    continue;
  }

  let content = readFileContent(located.file);

  // 检查是否已经包含目标端点
  if (content.includes(`"${patch.addPattern}"`)) {
    console.log(`[SKIP] ${patch.name} - already contains ${patch.addPattern}`);
    ssrfStats.already++;
    continue;
  }

  // 找到数组定义，添加新端点
  // 模式: 匹配数组中的最后一个元素后添加
  const patterns = [
    // 模式1: 在 "graph.microsoft.cn" 后添加
    {
      search: '"graph.microsoft.cn"\n  ];',
      replace: '"graph.microsoft.cn",\n\t"' + patch.addPattern + '"\n  ];'
    },
    // 模式2: 在数组末尾元素后添加 (带逗号)
    {
      search: /(const DEFAULT_MEDIA_HOST_ALLOWLIST = \[[^\]]+)("[^"]+"\n\s*\];)/,
      replace: (match) => match.replace(/("[^"]+"\n\s*\];)/, `$1,\n\t"${patch.addPattern}"\n  ];`)
    },
    // 模式3: 在数组末尾元素后添加 (不带逗号)
    {
      search: /(const DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST = \[[^\]]+)("[^"]+"\n\s*\];)/,
      replace: (match) => match.replace(/("[^"]+"\n\s*\];)/, `$1,\n\t"${patch.addPattern}"\n  ];`)
    }
  ];

  let patched = false;

  // 尝试简单字符串替换
  if (content.includes('"graph.microsoft.cn"\n  ];')) {
    content = content.replace(
      '"graph.microsoft.cn"\n  ];',
      '"graph.microsoft.cn",\n\t"' + patch.addPattern + '"\n  ];'
    );
    patched = true;
  } else if (content.includes('"graph.microsoft.cn"\n\t];')) {
    // 处理缩进差异
    content = content.replace(
      '"graph.microsoft.cn"\n\t];',
      '"graph.microsoft.cn",\n\t"' + patch.addPattern + '"\n  ];'
    );
    patched = true;
  }

  if (patched) {
    writeFileContent(located.file, content);
    console.log(`[OK]   ${patch.name} - added ${patch.addPattern}`);
    ssrfStats.patched++;
  } else {
    console.log(`[WARN] ${patch.name} - could not apply patch automatically`);
    console.log(`       Manual fix required: add "${patch.addPattern}" to ${located.file}`);
    ssrfStats.not_found++;
  }
}

console.log(`\nPhase 3 result: ${ssrfStats.patched} patched, ${ssrfStats.already} already, ${ssrfStats.not_found} failed\n`);

// ===== 第四阶段：验证 =====
console.log('Phase 4: Verification');
console.log('-'.repeat(40));

const verificationChecks = [
  { pattern: 'login.chinacloudapi.cn', desc: 'China AAD authority' },
  { pattern: 'api.botframework.azure.cn', desc: 'China Bot Framework API' },
  { pattern: 'login.botframework.azure.cn', desc: 'China Bot Framework login' },
  { pattern: 'token.botframework.azure.cn', desc: 'China Bot Framework token' },
  { pattern: 'microsoftgraph.chinacloudapi.cn', desc: 'China Graph API' },
];

let allPassed = true;

for (const check of verificationChecks) {
  let found = false;
  for (const file of fileList) {
    if (readFileContent(file).includes(check.pattern)) {
      found = true;
      break;
    }
  }
  
  if (found) {
    console.log(`[PASS] ${check.desc}`);
  } else {
    console.log(`[FAIL] ${check.desc} not found!`);
    allPassed = false;
  }
}

// 检查是否还有未替换的全局端点
const globalPatterns = [
  { pattern: 'login.botframework.com', exclude: 'login.botframework.azure.cn' },
  { pattern: 'token.botframework.com', exclude: null },
];

console.log('\nRemaining global endpoints check:');
for (const check of globalPatterns) {
  let count = 0;
  for (const file of fileList) {
    const content = readFileContent(file);
    if (content.includes(check.pattern)) {
      if (check.exclude && content.includes(check.exclude)) {
        continue; // 有对应的 CN 端点，OK
      }
      count++;
    }
  }
  if (count > 0) {
    console.log(`[WARN] ${check.pattern}: ${count} files still contain this pattern`);
  } else {
    console.log(`[OK]   ${check.pattern}: all replaced`);
  }
}

// ===== 最终结果 =====
console.log('\n' + '='.repeat(60));
const totalPatched = stats.patched + globalStats.patched + ssrfStats.patched;
if (totalPatched > 0) {
  console.log(`SUCCESS: ${totalPatched} patches applied.`);
  console.log('  - Phase 1 (Marker): ' + stats.patched + ' patches');
  console.log('  - Phase 2 (Global): ' + globalStats.patched + ' replacements');
  console.log('  - Phase 3 (SSRF):   ' + ssrfStats.patched + ' allowlist patches');
  console.log('\nIMPORTANT: You MUST restart the gateway now:');
  console.log('  openclaw gateway restart');
  console.log('\nDo NOT restart from a dialog box - use terminal/command line.');
} else {
  console.log('All patches already applied. No changes needed.');
}
console.log('='.repeat(60));

process.exit(allPassed ? 0 : 1);