#!/usr/bin/env node
// doctor.mjs — 无 AI 环境自检（quick 版；完整检查见 modes/doctor.md）
// 用法: node scripts/doctor.mjs [PROJECT_ROOT]
// 退出码: 0 = 健康（可有 ⚠️），1 = 存在 ⛔ 阻塞项

import { access, readdir, readFile, stat } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { SCAN_SCHEMA, PAGE_TYPES, RELIABILITY, SCAN_STATUS } from '../scrapers/_fields.mjs';
import { checkGranularity } from './lib/official-sources.mjs';

const root = process.argv[2] ?? join(dirname(fileURLToPath(import.meta.url)), '..');
const results = [];
const check = (level, name, msg) => results.push({ level, name, msg });

async function exists(p) {
  try { await access(p); return true; } catch { return false; }
}

// 分发副本模式：tools/package-skill.mjs 生成的 ClawHub skill 目录，根上有 SKILL.md
// 且不含仓库级文件（README/CLAUDE.md）与各客户端软链。这些在副本里缺失是设计如此，
// 不是故障——按副本口径跳过，否则装完跑 doctor 会白得 5 个 ⛔。
const isSkillPackage = await exists(join(root, 'SKILL.md'));
const REPO_ONLY_FILES = new Set(['CLAUDE.md', 'README.md', 'config/profile.example.yml']);
// 分发副本里 AGENTS.md 可以没有：`npx skills add` 只会带走 skill 目录内的东西，而 AGENTS.md
// 刻意不做软链（链了会让 Project Root 从仓库根掉进 skill 目录）。缺它只是失去自然语言路由，
// 不是故障——降为建议并说明后果，否则装完跑 doctor 会白得一个 ⛔。
const SOFT_FILES_IN_PACKAGE = new Set(['AGENTS.md']);

// 0. 运行时版本：核心脚本 Node ≥18 即可，TUI 因为 ink 依赖链（string-width 用 RegExp v flag）要 ≥20
{
  const major = Number(process.versions.node.split('.')[0]);
  check(major >= 18 ? 'pass' : 'fail', `Node ${process.versions.node}`,
    major >= 18 ? (major < 20 ? '核心脚本可用；dashboard（TUI）需要 ≥20' : '') : '低于最低要求 Node 18');
}

// 1. 系统层完整性
const sysFiles = [
  'AGENTS.md', 'CLAUDE.md', 'README.md',
  'modes/_shared.md', 'modes/intake.md', 'modes/evaluate.md',
  'modes/deep-dive.md', 'modes/negotiate.md', 'modes/watchlist.md',
  'modes/triage.md', 'modes/compare.md', 'modes/visit.md',
  'modes/contract.md', 'modes/doctor.md', 'modes/stats.md', 'modes/scan.md',
  'templates/policy-notes.cn.yml', 'templates/policy-notes.eu.yml', 'templates/policy-notes.apac.yml',
  'templates/contract-checklist.cn.yml',
  'templates/official-sources.cn.yml', 'templates/official-sources.eu.yml',
  'templates/official-sources.apac.yml',
  'config/profile.example.yml',
  'package.json',
  'scripts/reserve-report-num.mjs', 'scripts/doctor.mjs', 'scripts/stats.mjs',
  'scripts/scan.mjs', 'scripts/lib/data.mjs', 'scripts/lib/detect.mjs',
  'scripts/lib/official-sources.mjs', 'scripts/dashboard.mjs',
  'scripts/map.mjs',
  'scrapers/_registry.mjs', 'scrapers/_fields.mjs', 'scrapers/ADDING_A_PLATFORM.md',
];
for (const f of sysFiles) {
  if (isSkillPackage && REPO_ONLY_FILES.has(f)) continue;
  if (await exists(join(root, f))) {
    check('pass', `系统文件 ${f}`, '');
    continue;
  }
  if (isSkillPackage && SOFT_FILES_IN_PACKAGE.has(f)) {
    check('warn', `系统文件 ${f}`, '分发副本不含 AGENTS.md：自然语言触发不可用，请用 /house-ops <mode> 显式调用');
  } else {
    check('fail', `系统文件 ${f}`, '缺失');
  }
}

// 1b. 平台模块：registry 遇坏模块只打警告并跳过（识别静默降级 generic），doctor 必须把它变成阻塞项
{
  const expected = ['5i5j', 'anjuke', 'beike', 'fang', 'lianjia']; // 已登记平台的基线，缺一个即 ⛔
  const dir = join(root, 'scrapers');
  const files = (await readdir(dir).catch(() => [])).filter((f) => f.endsWith('.mjs') && !f.startsWith('_'));
  const broken = [];
  const ids = [];
  for (const f of files) {
    try {
      const mod = await import(pathToFileURL(join(dir, f)).href);
      const s = mod.default;
      if (!s || !s.id || typeof s.detect !== 'function') { broken.push(`${f}（default export 需为 { id, detect }）`); continue; }
      ids.push(s.id);
    } catch (err) {
      broken.push(`${f}（加载失败: ${err.message}）`);
    }
  }
  check(broken.length ? 'fail' : 'pass', `平台模块可加载（${files.length} 个）`,
    broken.length ? `${broken.join('; ')}——识别会静默退回 generic` : files.join(', '));
  const missing = expected.filter((id) => !ids.includes(id));
  check(missing.length ? 'fail' : 'pass', '平台模块基线',
    missing.length ? `缺失平台模块: ${missing.join(', ')}——识别会静默退回 generic，按 scrapers/ADDING_A_PLATFORM.md 补回`
      : `已登记 ${ids.length} 个（含基线 ${expected.join('/')}）`);
}

// 2. 技能符号链接（分发副本自带 SKILL.md，不需要各客户端软链）
if (isSkillPackage) {
  check('pass', '技能入口 SKILL.md', '分发副本模式：根目录即技能本体');
} else {
  for (const link of ['.claude/skills/house-ops', '.zcode/skills/house-ops']) {
    const p = join(root, link);
    let ok = false;
    try { ok = (await stat(p)).isDirectory() && (await exists(join(p, 'SKILL.md'))); } catch {}
    check(ok ? 'pass' : 'fail', `技能链接 ${link}`, ok ? '' : '不可解析或缺 SKILL.md');
  }
}

// 3. 用户层状态
const profileOk = await exists(join(root, 'config/profile.yml'));
check(profileOk ? 'pass' : 'warn', '需求画像 config/profile.yml',
  profileOk ? '' : '缺失 — 先运行 /house-ops intake');

// 4. 数据一致性：watchlist 编号 vs reports/
const reportsDir = join(root, 'reports');
const reportNums = new Set();
for (const f of await readdir(reportsDir).catch(() => [])) {
  const m = /^(\d{3})-/.exec(f);
  if (m && f.endsWith('.md')) reportNums.add(m[1]);
}
const watchlistPath = join(root, 'data/watchlist.md');
let orphanRows = [];
if (await exists(watchlistPath)) {
  const lines = (await readFile(watchlistPath, 'utf8')).split('\n');
  for (const line of lines) {
    if (!line.startsWith('|') || line.includes('---') || line.includes('编号')) continue;
    const cells = line.split('|').map(c => c.trim()).filter(Boolean);
    const no = cells[0];
    if (no && !/^\d{3}$/.test(no)) continue;
    if (no && !reportNums.has(no)) orphanRows.push(`${no}（无对应报告）`);
  }
  check(orphanRows.length ? 'warn' : 'pass', 'watchlist 一致性',
    orphanRows.length ? `异常行: ${orphanRows.join('; ')}` : 'watchlist 与报告编号/状态一致');
} else {
  check('warn', 'watchlist', '尚未创建（首次评估时自动生成）');
}

// 5. 政策表时效（中欧两张表都要看）
for (const f of ['templates/policy-notes.cn.yml', 'templates/policy-notes.eu.yml']) {
  try {
    const yml = await readFile(join(root, f), 'utf8');
    const m = /as_of_overview:\s*(\d{4})-(\d{2})-(\d{2})/.exec(yml);
    if (!m) continue;
    const ageDays = Math.floor((Date.now() - new Date(`${m[1]}-${m[2]}-${m[3]}`)) / 86400000);
    check(ageDays > 90 ? 'warn' : 'pass', `政策数据表时效 ${f.replace('templates/', '')}`,
      ageDays > 90 ? `as_of 已 ${ageDays} 天，建议核实更新` : `as_of ${ageDays} 天内`);
  } catch {}
}

// 6. scan schema 一致性：modes/scan.md（SoT 文本）与 _fields.mjs 导出的枚举断言
try {
  const scanDoc = await readFile(join(root, 'modes/scan.md'), 'utf8');
  const missing = [
    SCAN_SCHEMA,
    ...PAGE_TYPES,
    ...RELIABILITY,
    ...SCAN_STATUS,
  ].filter((token) => !scanDoc.includes(token));
  check(missing.length ? 'fail' : 'pass', 'scan schema 一致性（scan.md ↔ _fields.mjs）',
    missing.length ? `scan.md 缺少 schema token: ${missing.join(', ')}` : '');
} catch (err) {
  check('fail', 'scan schema 一致性', `读取失败: ${err.message}`);
}

// 6b. 政务源 granularity 枚举自一致（取值必须落在 SOURCE_GRANULARITIES 原子档内，多粒度用内联数组）
try {
  const g = await checkGranularity(root);
  check(g.bad.length ? 'fail' : 'pass', '政务源 granularity 枚举自一致',
    g.bad.length
      ? `${g.bad.length} 处漂移: ${g.bad.map((b) => `${b.file}/${b.city}="${Array.isArray(b.value) ? b.value.join(',') : b.value}"（非法: ${b.unknown.join(',')}）`).join('; ')}`
      : `${g.files.join(', ')} 共 ${g.checked} 条粒度取值合规`);
} catch (err) {
  check('fail', '政务源 granularity 枚举自一致', `读取失败: ${err.message}`);
}

// 7. 市场覆盖：登记表与政策表必须成对，且画像里的 market.code 要落在已登记市场内
{
  const tplFiles = await readdir(join(root, 'templates')).catch(() => []);
  const grab = (re) => tplFiles.map((f) => re.exec(f)?.[1]).filter(Boolean);
  const regMarkets = grab(/^official-sources\.(.+)\.yml$/);
  const polMarkets = grab(/^policy-notes\.(.+)\.yml$/);
  const codes = new Set(regMarkets);
  for (const f of regMarkets) {
    const text = await readFile(join(root, 'templates', `official-sources.${f}.yml`), 'utf8').catch(() => '');
    // 条目既可能是 `- market: uk`（列表起始行）也可能是 `  market: uk`（缩进键）
    for (const m of text.matchAll(/^\s*(?:-\s+)?market:\s*"?([a-z]{2})"?\s*(?:#.*)?$/gm)) codes.add(m[1]);
  }
  const unpaired = regMarkets.filter((m) => !polMarkets.includes(m));
  check(regMarkets.length && !unpaired.length ? 'pass' : 'warn', '市场覆盖',
    regMarkets.length
      ? `登记表 ${regMarkets.join(', ')}；可用市场码 ${[...codes].sort().join(', ')}${unpaired.length ? `（缺政策表: ${unpaired.join(', ')}）` : ''}`
      : '未发现 official-sources.<market>.yml');

  if (profileOk) {
    const txt = await readFile(join(root, 'config/profile.yml'), 'utf8').catch(() => '');
    const mc = /^ {2}code:\s*"?([a-z]{2})"?\s*(?:#.*)?$/m.exec(txt)?.[1];
    check(mc && codes.has(mc) ? 'pass' : 'warn', `画像市场码 ${mc ?? '未设置'}`,
      mc ? (codes.has(mc) ? '' : `不在已登记市场内（${[...codes].sort().join(', ')}）`) : 'config/profile.yml 未设 market.code — 跑 /house-ops intake');
  }
}

// 汇总输出
let fails = 0, warns = 0;
for (const r of results) {
  const icon = r.level === 'pass' ? '✅' : r.level === 'warn' ? '⚠️ ' : '⛔';
  if (r.level === 'fail') fails++;
  if (r.level === 'warn') warns++;
  console.log(`${icon} ${r.name}${r.msg ? ' — ' + r.msg : ''}`);
}
console.log(`\n${fails ? `${fails} 项阻塞，` : ''}${warns ? `${warns} 项建议` : ''}${!fails && !warns ? '环境健康' : ''}`);
process.exit(fails ? 1 : 0);
