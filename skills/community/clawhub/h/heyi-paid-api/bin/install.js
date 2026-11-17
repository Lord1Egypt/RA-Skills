#!/usr/bin/env node
/* eslint-disable no-console */

'use strict';

const fs = require('fs');
const https = require('https');
const http = require('http');
const os = require('os');
const path = require('path');
const { URL } = require('url');

const SKILL_NAME = 'heyi-paid-api';
const SKILL_SOURCE_FILE = 'SKILL.md';
const SNAPSHOT_FILE = 'snapshots/catalog.json';
const DEFAULT_BASE_URL = 'https://bot.01011.top';
const SNAPSHOT_VERSION = 1;

// 统一的 SKILL.md 格式说明：所有 agent 都遵循 Agent Skills 规范，
// 只是目录位置不同。这里集中维护路由表，新增 agent 只需加一行。
const AGENTS = [
  {
    id: 'claude',
    label: 'Claude Code',
    home: () => path.join(os.homedir(), '.claude'),
    userPath: () => path.join(os.homedir(), '.claude', 'skills', SKILL_NAME),
    projectPath: (cwd) => path.join(cwd, '.claude', 'skills', SKILL_NAME),
  },
  {
    id: 'codex',
    label: 'Codex',
    home: () => path.join(os.homedir(), '.agents'),
    userPath: () => path.join(os.homedir(), '.agents', 'skills', SKILL_NAME),
    projectPath: (cwd) => path.join(cwd, '.agents', 'skills', SKILL_NAME),
  },
  {
    id: 'cursor',
    label: 'Cursor',
    // Cursor 的 settings/skills 都在 ~/.cursor/ 下；skills-cursor/ 是内置保留区，不能写。
    home: () => path.join(os.homedir(), '.cursor'),
    userPath: () => path.join(os.homedir(), '.cursor', 'skills', SKILL_NAME),
    projectPath: (cwd) => path.join(cwd, '.cursor', 'skills', SKILL_NAME),
  },
  {
    id: 'openclaw',
    label: 'OpenClaw',
    home: () => path.join(os.homedir(), '.openclaw'),
    userPath: () => path.join(os.homedir(), '.openclaw', 'skills', SKILL_NAME),
    projectPath: (cwd) => path.join(cwd, '.openclaw', 'skills', SKILL_NAME),
  },
  {
    id: 'mavis',
    label: 'Mavis',
    home: () => path.join(os.homedir(), '.mavis'),
    userPath: () => path.join(os.homedir(), '.mavis', 'skills', SKILL_NAME),
    projectPath: (cwd) => path.join(cwd, '.mavis', 'skills', SKILL_NAME),
  },
];

// ----------------------------------------------------------------------------
// Argument parsing
// ----------------------------------------------------------------------------

function parseArgs(argv) {
  // 支持子命令：argv[2] 可以是 install / check / snapshot / help。
  // 没有子命令时按 install 默认行为（保持向后兼容）。
  const args = {
    command: 'install',
    force: false,
    dryRun: false,
    help: false,
    project: false,
    target: null,
    agents: null, // null = 自动检测；字符串列表 = 仅装指定 agent
    all: false,
    strict: false,
    baseUrl: null,
    snapshotPath: null,
    version: false,
  };

  let i = 2;
  // 第一个非 - 前缀参数当子命令
  if (i < argv.length && argv[i] && !argv[i].startsWith('-')) {
    const candidate = argv[i];
    if (['install', 'check', 'snapshot', 'help'].includes(candidate)) {
      args.command = candidate;
      i += 1;
    }
  }

  for (; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '-h' || arg === '--help') {
      args.help = true;
    } else if (arg === '--version' || arg === '-V') {
      args.version = true;
    } else if (arg === '-f' || arg === '--force') {
      args.force = true;
    } else if (arg === '-n' || arg === '--dry-run') {
      args.dryRun = true;
    } else if (arg === '--project') {
      args.project = true;
    } else if (arg === '--all') {
      args.all = true;
    } else if (arg === '--strict') {
      args.strict = true;
    } else if (arg === '--agent' || arg === '-a') {
      const value = argv[i + 1];
      if (!value) {
        console.error('错误：--agent 需要指定 agent id（逗号分隔）');
        process.exit(2);
      }
      args.agents = value.split(',').map((s) => s.trim()).filter(Boolean);
      i += 1;
    } else if (arg === '--target' || arg === '-t') {
      args.target = argv[i + 1];
      i += 1;
    } else if (arg === '--base-url' || arg === '-b') {
      args.baseUrl = argv[i + 1];
      i += 1;
    } else if (arg === '--snapshot' || arg === '-s') {
      args.snapshotPath = argv[i + 1];
      i += 1;
    } else if (!arg.startsWith('-') && args.command === 'install') {
      // 向后兼容：install 子命令下，未知非 - 参数当 --target
      args.target = arg;
    } else {
      console.error(`未知参数: ${arg}`);
      process.exit(2);
    }
  }
  return args;
}

function resolveBaseUrl(args) {
  return (args.baseUrl || process.env.HEYI_API_BASE_URL || DEFAULT_BASE_URL).replace(/\/+$/, '');
}

function printVersion() {
  const pkg = readPackageJson();
  console.log(`${pkg.name} ${pkg.version}`);
}

function printHelp() {
  const lines = [
    `install-heyi-paid-api-skill — 安装 heyi-paid-api Skill 到 Cursor / Claude Code / Codex / OpenClaw`,
    '',
    '用法:',
    `  install-heyi-paid-api-skill [install 子命令选项]`,
    `  install-heyi-paid-api-skill check [--strict] [--base-url <url>]`,
    `  install-heyi-paid-api-skill snapshot [--base-url <url>] [--snapshot <path>]`,
    '',
    '子命令:',
    `  install (默认)   把 SKILL.md 复制到各 agent 的 skills 目录`,
    `  check           拉取远端公开目录，与 npm 包内嵌快照对比`,
    `  snapshot        重新生成 snapshots/catalog.json（开发期使用）`,
    `  help            显示本帮助`,
    '',
    'install 子命令选项:',
    '  --all                  忽略本机是否安装，全部 5 个 agent 都装（全局用户级）',
    '  -a, --agent <list>     只装指定 agent，逗号分隔。可用: claude,codex,cursor,openclaw,mavis',
    `  --project              装到当前项目（.claude/.agents/.cursor/.openclaw/skills/${SKILL_NAME}/）`,
    '  -t, --target <dir>     装到任意指定目录（绕过 agent 路由表，单点安装）',
    '  -f, --force            覆盖已存在的 skill 目录',
    '  -n, --dry-run          只打印计划，不实际写入',
    '  -h, --help             显示帮助',
    '',
    'check 子命令选项:',
    '  --strict               added（新增）也退出码 1（默认仅 retired/changed 报错）',
    '  --base-url <url>       覆盖远端 base URL（默认 $HEYI_API_BASE_URL，回落到 https://bot.01011.top）',
    '  -h, --help             显示帮助',
    '',
    'snapshot 子命令选项:',
    '  --base-url <url>       远端 base URL（默认同上）',
    '  --snapshot <path>      快照输出路径（默认 <pkg>/snapshots/catalog.json）',
    '  -h, --help             显示帮助',
    '',
    '退出码（check）:',
    '  0   一致，或仅 added（soft）',
    '  1   发现 retired / changed（--strict 时 added 也算）',
    '  2   网络/HTTP/JSON 解析失败，或快照文件缺失',
    '',
    '支持的目标 agent:',
  ];
  AGENTS.forEach((a) => {
    lines.push(`  ${a.id.padEnd(8)} ${a.label.padEnd(14)} → ${a.userPath().replace(os.homedir(), '~')}`);
  });
  console.log(lines.join('\n'));
}

// ----------------------------------------------------------------------------
// Install subcommand (原有逻辑，行为不变)
// ----------------------------------------------------------------------------

function resolveSourceFile() {
  // 兼容多种入口：
  //   1. npx 安装到 npx 缓存后，bin/install.js 与 SKILL.md 同目录（标准）
  //   2. 直接 node bin/install.js（开发场景）
  //   3. 仓库根目录直接跑（罕见）
  const candidates = [
    path.join(__dirname, '..', SKILL_SOURCE_FILE),
    path.join(__dirname, SKILL_SOURCE_FILE),
    path.join(process.cwd(), SKILL_SOURCE_FILE),
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  return null;
}

function copyDir(srcDir, destDir) {
  // 当前 skill 仅一个 SKILL.md，但保留目录复制能力，便于未来扩展。
  fs.mkdirSync(destDir, { recursive: true });
  for (const entry of fs.readdirSync(srcDir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    if (entry.name === 'node_modules') continue;
    if (entry.name === SNAPSHOT_FILE.split('/')[0]) continue; // 不覆盖用户目标的 snapshots/
    const srcPath = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else if (entry.isFile()) {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function detectInstalledAgents() {
  // 本机 ~/.claude 等目录存在即视为已装对应 agent。
  return AGENTS.filter((a) => {
    try {
      return fs.existsSync(a.home());
    } catch (_) {
      return false;
    }
  });
}

function resolveInstallTargets(args) {
  // 单点 target 优先于 agent 路由表。
  if (args.target) {
    return [{ id: 'custom', label: 'Custom', dir: path.resolve(args.target) }];
  }

  let selectedAgents;
  if (args.agents) {
    // 用户显式指定 agent
    const ids = new Set(args.agents);
    const invalid = [...ids].filter((id) => !AGENTS.some((a) => a.id === id));
    if (invalid.length > 0) {
      console.error(`错误：未知 agent id: ${invalid.join(', ')}`);
      console.error(`可用: ${AGENTS.map((a) => a.id).join(', ')}`);
      process.exit(2);
    }
    selectedAgents = AGENTS.filter((a) => ids.has(a.id));
  } else if (args.all) {
    selectedAgents = AGENTS.slice();
  } else {
    // 自动检测
    selectedAgents = detectInstalledAgents();
  }

  if (selectedAgents.length === 0) {
    return [];
  }

  const cwd = process.cwd();
  return selectedAgents.map((a) => ({
    id: a.id,
    label: a.label,
    dir: args.project ? a.projectPath(cwd) : a.userPath(),
  }));
}

function runInstall(args) {
  const sourceFile = resolveSourceFile();
  if (!sourceFile) {
    console.error('错误：找不到 SKILL.md。请通过 npx 安装，或在包根目录运行此脚本。');
    process.exit(1);
  }
  const sourceDir = path.dirname(sourceFile);

  const targets = resolveInstallTargets(args);

  if (targets.length === 0) {
    console.error('未检测到任何已安装的 agent。');
    console.error('本机会话下 ~/.claude/、~/.agents/、~/.cursor/、~/.openclaw/ 都不存在。');
    console.error('');
    console.error('可选操作:');
    console.error('  --all         强制装到全部 5 个 agent 的全局目录（无需先装 agent）');
    console.error('  --agent <id>  强制装到指定 agent 的全局目录（无需先装 agent）');
    console.error('  --target <dir> 装到任意指定目录');
    process.exit(1);
  }

  // 冲突检测（除非 --force）。dry-run 只提示，不退出——用户想看的是计划本身。
  if (!args.force) {
    const conflicts = targets.filter((t) => fs.existsSync(t.dir));
    if (conflicts.length > 0) {
      const log = args.dryRun ? console.log : console.error;
      log(args.dryRun
        ? '以下目标目录已存在，实际安装时需加 --force 覆盖：'
        : '以下目标目录已存在，请加 --force 覆盖：');
      conflicts.forEach((t) => log(`  - ${t.dir} (${t.label})`));
      if (!args.dryRun) {
        process.exit(1);
      }
      log('');
    }
  }

  console.log('heyi-paid-api Skill 安装计划');
  console.log('================================');
  console.log(`  源目录:   ${sourceDir}`);
  console.log(`  模式:     ${args.dryRun ? 'dry-run' : 'install'}`);
  console.log(`  范围:     ${args.project ? 'project (当前目录)' : 'user (全局)'}`);
  console.log(`  覆盖:     ${args.force ? 'yes' : 'no'}`);
  console.log(`  目标数:   ${targets.length}`);
  console.log('');
  targets.forEach((t) => {
    console.log(`  → [${t.id}] ${t.label.padEnd(14)} ${t.dir}`);
  });
  console.log('');

  if (args.dryRun) {
    console.log('[dry-run] 未实际写入文件。');
    return;
  }

  targets.forEach((t) => {
    copyDir(sourceDir, t.dir);
  });

  console.log('安装完成 ✓');
  console.log('');
  console.log('下一步：');
  console.log('  1. 重启对应的 agent（或让 agent 自动重载 Skills，参见各 agent 文档）。');
  console.log('  2. 在 agent 中提一个使用 heyi-paid-api skill 的问题，确认自动加载。');
  console.log('  3. 运行 `npx heyihub-skill check` 验证本地 Skill 快照与远端接口目录是否一致。');
  console.log('');
  console.log('如需卸载：直接删除上面列出的目录即可。');
}

// ----------------------------------------------------------------------------
// Snapshot & check subcommands
// ----------------------------------------------------------------------------

function readPackageJson() {
  const candidates = [
    path.join(__dirname, '..', 'package.json'),
    path.join(process.cwd(), 'package.json'),
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return JSON.parse(fs.readFileSync(candidate, 'utf8'));
    }
  }
  // 兜底：尽量返回可读的 name/version，避免完全崩
  return { name: 'heyihub-skill', version: '0.0.0' };
}

function resolveSnapshotPath(args) {
  if (args.snapshotPath) {
    return path.resolve(args.snapshotPath);
  }
  // 默认 <pkg>/snapshots/catalog.json；优先 package.json 同级目录
  const candidates = [
    path.join(__dirname, '..', SNAPSHOT_FILE),
    path.join(process.cwd(), SNAPSHOT_FILE),
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate) || fs.existsSync(path.dirname(candidate))) {
      return candidate;
    }
  }
  return path.join(__dirname, '..', SNAPSHOT_FILE);
}

// 零依赖 HTTP 客户端（兼容 Node 14，无 globalThis.fetch）
function fetchJson(targetUrl, opts) {
  const { maxRedirects = 3, timeoutMs = 8000 } = opts || {};
  return new Promise((resolve, reject) => {
    let redirects = 0;
    const visit = (url) => {
      let parsed;
      try {
        parsed = new URL(url);
      } catch (err) {
        reject(new Error(`URL 不合法: ${url}`));
        return;
      }
      const lib = parsed.protocol === 'http:' ? http : https;
      const req = lib.get(parsed, (res) => {
        const status = res.statusCode || 0;
        if (status >= 301 && status <= 308 && res.headers.location) {
          if (redirects >= maxRedirects) {
            reject(new Error(`重定向次数超过 ${maxRedirects} 次`));
            return;
          }
          redirects += 1;
          res.resume();
          const next = new URL(res.headers.location, parsed).toString();
          visit(next);
          return;
        }
        if (status < 200 || status >= 300) {
          res.resume();
          reject(new Error(`HTTP ${status}`));
          return;
        }
        const chunks = [];
        res.on('data', (chunk) => chunks.push(chunk));
        res.on('end', () => {
          const body = Buffer.concat(chunks).toString('utf8');
          try {
            resolve(JSON.parse(body));
          } catch (err) {
            reject(new Error(`响应不是合法 JSON: ${err.message}`));
          }
        });
      });
      req.setTimeout(timeoutMs, () => {
        req.destroy(new Error(`请求超时（${timeoutMs}ms）`));
      });
      req.on('error', (err) => reject(err));
    };
    visit(targetUrl);
  });
}

function normalizeRemoteEndpoint(ep) {
  // 来自 apps/api/views/public_platform_views.py 的 _serialize_endpoint（include_schema=False）
  return {
    code: ep.code,
    method: ep.method,
    path: ep.path,
    name: ep.name,
    category: ep.category || null,
    category_display: ep.category_display || null,
    group_code: ep.group_code || null,
    original_price_points: typeof ep.original_price_points === 'number' ? ep.original_price_points : null,
    effective_price_points: typeof ep.effective_price_points === 'number' ? ep.effective_price_points : null,
    discount_percent: typeof ep.discount_percent === 'number' ? ep.discount_percent : null,
  };
}

async function buildRemoteSnapshot(baseUrl) {
  const url = `${baseUrl}/api/external/platform/public/endpoints/`;
  const payload = await fetchJson(url);
  const endpoints = Array.isArray(payload && payload.data && payload.data.endpoints)
    ? payload.data.endpoints.map(normalizeRemoteEndpoint)
    : [];
  // 按 (group_code, category, path, method) 排序，输出更稳定
  endpoints.sort((a, b) => {
    return (
      String(a.group_code).localeCompare(String(b.group_code)) ||
      String(a.category).localeCompare(String(b.category)) ||
      String(a.path).localeCompare(String(b.path)) ||
      String(a.method).localeCompare(String(b.method))
    );
  });
  return {
    version: SNAPSHOT_VERSION,
    base_url: baseUrl,
    fetched_at: new Date().toISOString(),
    endpoints,
  };
}

function loadSnapshot(snapshotPath) {
  if (!fs.existsSync(snapshotPath)) {
    const err = new Error(`快照文件不存在: ${snapshotPath}。请先运行 \`snapshot\` 子命令生成。`);
    err.code = 'SNAPSHOT_MISSING';
    throw err;
  }
  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
  } catch (err) {
    const wrap = new Error(`快照 JSON 解析失败: ${err.message}`);
    wrap.code = 'SNAPSHOT_INVALID';
    throw wrap;
  }
  if (parsed.version !== SNAPSHOT_VERSION || !Array.isArray(parsed.endpoints)) {
    const err = new Error(`快照 schema 不符合 version=${SNAPSHOT_VERSION}（当前 ${parsed.version}）。`);
    err.code = 'SNAPSHOT_INVALID';
    throw err;
  }
  return parsed;
}

// 构造 diff 的可比索引：(code, method, path) 三元组。
// SKILL.md 协议要求 agent 按 code 调用，path/method 是后端契约。
const COMPARABLE_FIELDS = [
  'method',
  'path',
  'category',
  'group_code',
  'original_price_points',
  'effective_price_points',
  'discount_percent',
];

function indexEndpoints(endpoints) {
  const map = new Map();
  for (const ep of endpoints) {
    if (!ep || !ep.code) continue;
    map.set(ep.code, ep);
  }
  return map;
}

function diffSnapshots(local, remote) {
  const localMap = indexEndpoints(local.endpoints);
  const remoteMap = indexEndpoints(remote.endpoints);
  const retired = [];
  const added = [];
  const changed = [];

  for (const [code, localEp] of localMap.entries()) {
    const remoteEp = remoteMap.get(code);
    if (!remoteEp) {
      retired.push({
        code,
        method: localEp.method,
        path: localEp.path,
        name: localEp.name,
      });
      continue;
    }
    const fieldDiffs = [];
    for (const field of COMPARABLE_FIELDS) {
      const lv = localEp[field];
      const rv = remoteEp[field];
      if (lv !== rv) {
        fieldDiffs.push({ field, local: lv, remote: rv });
      }
    }
    if (fieldDiffs.length > 0) {
      changed.push({ code, name: remoteEp.name || localEp.name, fieldDiffs });
    }
  }

  for (const [code, remoteEp] of remoteMap.entries()) {
    if (!localMap.has(code)) {
      added.push({
        code,
        method: remoteEp.method,
        path: remoteEp.path,
        name: remoteEp.name,
      });
    }
  }

  // 稳定排序
  const byCode = (a, b) => String(a.code).localeCompare(String(b.code));
  retired.sort(byCode);
  added.sort(byCode);
  changed.sort(byCode);

  return { retired, added, changed };
}

function printDiff(diff, opts) {
  const { strict, local, remote } = opts;
  const { retired, added, changed } = diff;

  console.log('');
  console.log(`  本地快照: ${local.endpoints.length} 个接口（${local.fetched_at || 'unknown'}）`);
  console.log(`  远端目录: ${remote.endpoints.length} 个接口（${remote.fetched_at}）`);
  console.log('');

  if (retired.length === 0 && added.length === 0 && changed.length === 0) {
    console.log(`  ✓ ${remote.endpoints.length} 个接口全部一致，无需操作。`);
    console.log('');
    return { exitCode: 0, fail: false };
  }

  if (retired.length > 0) {
    console.log(`  ⚠ retired（已下线，本地快照有但远端缺） ${retired.length} 项：`);
    for (const ep of retired) {
      console.log(`    - ${ep.code}  ${ep.method} ${ep.path}  (${ep.name || ''})`);
    }
    console.log('');
  }

  if (changed.length > 0) {
    console.log(`  ⚠ changed（契约字段变动） ${changed.length} 项：`);
    for (const item of changed) {
      console.log(`    - ${item.code} (${item.name || ''})`);
      for (const f of item.fieldDiffs) {
        console.log(`        ${f.field}: ${JSON.stringify(f.local)} → ${JSON.stringify(f.remote)}`);
      }
    }
    console.log('');
  }

  if (added.length > 0) {
    console.log(`  ℹ added（新增，远端有但本地快照没有） ${added.length} 项：`);
    for (const ep of added) {
      console.log(`    + ${ep.code}  ${ep.method} ${ep.path}  (${ep.name || ''})`);
    }
    console.log('');
  }

  const hasFail = retired.length > 0 || changed.length > 0 || (strict && added.length > 0);
  if (hasFail) {
    console.log('  修复建议：');
    if (retired.length > 0 || changed.length > 0) {
      console.log('    1. 升级 Skill：`npx heyihub-skill@latest`，或在维护侧重新运行 `snapshot`');
      console.log('    2. 同步更新 SKILL.md 中相关章节（如有硬编码示例）');
    }
    if (added.length > 0 && !strict) {
      console.log('    added 默认不阻塞；若需严格 CI，加 `--strict`');
    }
    console.log('');
  }

  return { exitCode: hasFail ? 1 : 0, fail: hasFail };
}

async function runCheck(args) {
  const baseUrl = resolveBaseUrl(args);
  const snapshotPath = resolveSnapshotPath(args);

  console.log('heyi-paid-api Skill 运行期自检');
  console.log('================================');
  console.log(`  Base URL:    ${baseUrl}`);
  console.log(`  快照文件:    ${snapshotPath}`);
  console.log(`  模式:        ${args.strict ? 'strict' : 'soft'}`);

  let local;
  try {
    local = loadSnapshot(snapshotPath);
  } catch (err) {
    console.error('');
    console.error(`  ✗ ${err.message}`);
    process.exit(2);
  }

  let remote;
  try {
    remote = await buildRemoteSnapshot(baseUrl);
  } catch (err) {
    console.error('');
    console.error(`  ✗ 拉取远端公开目录失败: ${err.message}`);
    console.error('  提示：检查网络、`HEYI_API_BASE_URL`、或加 `--base-url <url>` 重试。');
    process.exit(2);
  }

  const diff = diffSnapshots(local, remote);
  const { exitCode } = printDiff(diff, { strict: args.strict, local, remote });
  process.exit(exitCode);
}

async function runSnapshot(args) {
  const baseUrl = resolveBaseUrl(args);
  const outputPath = resolveSnapshotPath(args);

  console.log('heyi-paid-api Skill snapshot 生成');
  console.log('================================');
  console.log(`  Base URL:    ${baseUrl}`);
  console.log(`  输出路径:    ${outputPath}`);

  let snapshot;
  try {
    snapshot = await buildRemoteSnapshot(baseUrl);
  } catch (err) {
    console.error('');
    console.error(`  ✗ 拉取远端公开目录失败: ${err.message}`);
    process.exit(2);
  }

  try {
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, `${JSON.stringify(snapshot, null, 2)}\n`, 'utf8');
  } catch (err) {
    console.error('');
    console.error(`  ✗ 写入快照失败: ${err.message}`);
    process.exit(2);
  }

  console.log('');
  console.log(`  ✓ 已写入 ${snapshot.endpoints.length} 个接口到 ${outputPath}`);
  console.log(`  fetched_at: ${snapshot.fetched_at}`);
  console.log('');
  console.log('  下一步：');
  console.log('    1. git diff 复核快照内容');
  console.log('    2. 提交并发布新版本 npm 包，让用户机器上的 check 拿到新基准');
}

// ----------------------------------------------------------------------------
// Entry / router
// ----------------------------------------------------------------------------

async function main() {
  const args = parseArgs(process.argv);

  if (args.help) {
    printHelp();
    process.exit(0);
  }
  if (args.version) {
    printVersion();
    process.exit(0);
  }

  if (args.command === 'help') {
    printHelp();
    process.exit(0);
  }
  if (args.command === 'check') {
    if (args.help) printHelp();
    await runCheck(args);
    return;
  }
  if (args.command === 'snapshot') {
    if (args.help) printHelp();
    await runSnapshot(args);
    return;
  }
  // install（默认）
  runInstall(args);
}

try {
  main();
} catch (err) {
  console.error(`执行失败: ${err && err.message ? err.message : err}`);
  if (err && err.stack) {
    console.error(err.stack);
  }
  process.exit(1);
}