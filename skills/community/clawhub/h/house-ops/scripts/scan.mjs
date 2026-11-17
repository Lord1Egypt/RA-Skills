#!/usr/bin/env node
// scan.mjs — 房源平台识别 / 扫描记录归一化 / 挂牌-成交交叉验证 / 政务数据源查询 / 价格历史
// 零依赖（Node ≥18）。平台模板见 scrapers/（career-ops providers 模式：一平台一模块）。
// schema SoT：modes/scan.md「扫描记录 schema」节。
// 用法:
//   node scripts/scan.mjs detect <url> [url...]          # 识别平台/页面类型，输出提取清单（平台负载去重，>3 条提示分批）
//   node scripts/scan.mjs normalize <record.json | ->    # 价格归一化 + 一致性检查（记录走 stdout，警告走 stderr）
//   node scripts/scan.mjs crosscheck <record.json> [--write]  # 挂牌价 vs 成交价交叉验证（含归一化；status=partial 走 stderr 提醒）
//   node scripts/scan.mjs official [关键词] [--market cn|eu]   # 查政务公开数据源登记表（默认跨全部登记文件）
//   node scripts/scan.mjs history [关键词] [--stale-days N]   # 无参=追踪时效表；关键词=单房源时间线与策略信号
//   node scripts/scan.mjs verify <record.json> [--evidence ev.json]  # 真实性验证（判定表输出 + provenance 建议）

import { readFile, writeFile, readdir } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadScrapers, detectPlatform } from '../scrapers/_registry.mjs';
import { COMMON_LISTING_FIELDS, normalizeRecord, finalizeRecord, buildEntityHistory, matchRecord, verifyAuthenticity } from '../scrapers/_fields.mjs';
import { evidenceSave, EVIDENCE_TYPES } from './evidence.mjs';
import { analyze } from './analysis.mjs';
import { groupDetections, overBudgetWarning } from './lib/detect.mjs';
import { readOfficialSources, filterSources } from './lib/official-sources.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

// 未识别平台的兜底提取清单 = 通用清单派生（不维护第二份手抄）
const GENERIC_FIELDS = COMMON_LISTING_FIELDS;

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString('utf8');
}

async function readJsonInput(arg) {
  let text;
  if (arg === '-' || arg === undefined) {
    if (process.stdin.isTTY) {
      console.error('用法: node scripts/scan.mjs normalize <record.json | ->（记录 JSON 走文件或 stdin 管道）');
      process.exit(1);
    }
    text = await readStdin();
  } else {
    text = await readFile(arg, 'utf8').catch((err) => {
      console.error(err.code === 'ENOENT' ? `⛔ 文件不存在: ${arg}` : `⛔ 读取失败: ${err.message}`);
      process.exit(1);
    });
  }
  try {
    return JSON.parse(text);
  } catch {
    console.error('⛔ 输入不是合法的 JSON——扫描记录 schema 见 modes/scan.md');
    process.exit(1);
  }
}

async function cmdDetect(urls) {
  if (!urls.length) {
    console.error('用法: node scripts/scan.mjs detect <url> [url...]');
    process.exitCode = 1;
    return;
  }
  const scrapers = await loadScrapers(join(ROOT, 'scrapers'));
  const items = urls.map((url) => {
    const found = detectPlatform(url, scrapers);
    if (!found) {
      return {
        url,
        platform: 'generic',
        name: '未识别平台',
        page_type: 'unknown',
        city_code: null,
        listing_id: null,
        fields: GENERIC_FIELDS,
        hint: '未命中已知平台模板——按通用清单提取，可靠度最高按「挂牌数据」并注明来源。新平台可按 scrapers/ADDING_A_PLATFORM.md 补模板。',
      };
    }
    const { scraper, hit } = found;
    return {
      url,
      platform: scraper.id,
      name: scraper.name,
      page_type: hit.page_type,
      city_code: hit.city_code ?? null,
      listing_id: hit.listing_id ?? null,
      fields: scraper.fields,
      transaction: scraper.transaction,
      notes: scraper.notes,
    };
  });
  // 平台负载（fields/transaction/notes）每平台只输出一次，URL 以清单挂在平台下（token 经济）
  const out = groupDetections(items);
  if (out.over_budget) console.error(overBudgetWarning(out.url_count));
  console.log(JSON.stringify(out, null, 2));
}

async function cmdNormalize(arg) {
  const raw = await readJsonInput(arg);
  const { record, warnings } = normalizeRecord(raw);
  warnings.forEach((w) => console.error(`⚠️  ${w}`));
  console.log(JSON.stringify(record, null, 2));
}

async function cmdCrosscheck(arg, write) {
  if (write && (arg === '-' || arg === undefined)) {
    console.error('⛔ --write 需要文件路径；stdin（-）输入只输出到 stdout');
    process.exit(1);
  }
  const raw = await readJsonInput(arg);
  // finalizeRecord：归一化 + 定价交叉验证一次完成（两步顺序约定已收进模块）
  const { record, warnings } = finalizeRecord(raw);
  warnings.forEach((w) => console.error(`⚠️  ${w}`));
  const out = JSON.stringify(record, null, 2);
  if (write) {
    await writeFile(arg, `${out}\n`);
    console.error(`✅ 定稿结果已写回 ${arg}`);
  } else {
    console.log(out);
  }
}

// 价格历史：无参 = 全部追踪键的时效表；带关键词 = 单键时间线与策略信号（数值由 _fields 计算）
async function cmdHistory(arg) {
  const argv = process.argv.slice(2);
  let staleDays = 14;
  if (argv.includes('--stale-days')) staleDays = Number(argv[argv.indexOf('--stale-days') + 1]) || 14;
  const dir = join(ROOT, 'data', 'scans');
  const files = (await readdir(dir).catch(() => [])).filter((f) => f.endsWith('.json'));
  const records = [];
  for (const f of files) {
    try {
      records.push(JSON.parse(await readFile(join(dir, f), 'utf8')));
    } catch {
      console.error(`⚠️  跳过无法解析的扫描记录: ${f}`);
    }
  }
  const entities = buildEntityHistory(records, { staleDays });
  if (!arg || arg.startsWith('--')) {
    if (!entities.length) {
      console.log('data/scans/ 下还没有扫描记录。');
      return;
    }
    console.log(`追踪房源实体时效（阈值 ${staleDays} 天，可在 modes/_custom.md 覆盖；实体 = 同一套房，可跨平台/重挂多挂牌键）：`);
    for (const e of entities) {
      const s = e.summary;
      console.log(`${s.stale ? '⚠️ ' : '✅'} ${e.community}（${e.district}）— 上次实采 ${s.last_date}（${s.days_since_last_capture} 天前）· 挂牌键×${s.listing_count}${s.cross_platform ? '（跨平台）' : ''} · ${s.listing_keys.join(', ')}`);
    }
    const stale = entities.filter((e) => e.summary.stale);
    if (stale.length) console.log(`\n💡 ${stale.length} 套房源实采已过期——建议快速复扫（仅采变动字段：总价/调价次数/带看/在售状态）。`);
    return;
  }
  const hit = entities.filter((e) =>
    (e.community ?? '').includes(arg)
    || e.summary.listing_keys.some((k) => k.includes(arg))
    || (e.fingerprint?.area != null && String(e.fingerprint.area) === arg));
  if (!hit.length) {
    console.log(`未找到匹配「${arg}」的房源实体（现有：${entities.map((e) => e.community).join('，') || '无'}）。`);
    process.exitCode = 2;
    return;
  }
  for (const e of hit) {
    console.log(JSON.stringify(e, null, 2));
  }
}

// 证据归档：户型图/政府公示/政策 PDF 等文件落盘 + 登记进扫描记录 evidence 数组
async function cmdEvidence(argv) {
  const action = argv[0];
  if (action === 'save') {
    const recPath = argv[1], type = argv[2], src = argv[3];
    const noteIdx = argv.indexOf('--note');
    const nameIdx = argv.indexOf('--name');
    const refererIdx = argv.indexOf('--referer');
    if (!recPath || !type || !src) {
      console.error('用法: node scripts/scan.mjs evidence save <record.json> <type> <文件路径或URL> [--note 备注] [--name 自定义文件名] [--referer URL]');
      console.error(`  type ∈ ${EVIDENCE_TYPES.join(' | ')}`);
      process.exit(1);
    }
    const out = await evidenceSave({
      recordPath: recPath, type, src,
      note: noteIdx > 0 ? argv[noteIdx + 1] : '',
      name: nameIdx > 0 ? argv[nameIdx + 1] : '',
      referer: refererIdx > 0 ? argv[refererIdx + 1] : '',
      scansDir: join(ROOT, 'data', 'scans'),
      evidenceDir: join(ROOT, 'data', 'evidence'),
      policyDir: join(ROOT, 'data', 'policy'),
    });
    console.log(`✅ 已归档: ${out.savedPath}`);
    console.log(`   evidence[${out.index}] type=${out.entry.type} → 记录已更新`);
    return;
  }
  if (action === 'list') {
    const recPath = argv[1];
    if (!recPath) { console.error('用法: node scripts/scan.mjs evidence list <record.json>'); process.exit(1); }
    const rec = await readJsonInput(recPath);
    const items = rec.evidence ?? [];
    if (!items.length) { console.log('（该记录暂无归档证据）'); return; }
    for (const [i, e] of items.entries()) console.log(`  [${i}] ${e.type} ${e.path}${e.note ? ' — ' + e.note : ''}（${e.captured_at}）`);
    return;
  }
  console.error('用法: node scripts/scan.mjs evidence <save|list> …');
  process.exit(1);
}

// 分类分析：六大类型（户型/流动性/日照采光/噪音/价格/真实性）结论 + 三句话观点提炼
async function cmdAnalyze(arg, evPath) {
  if (!arg) {
    console.error('用法: node scripts/scan.mjs analyze <record.json> [--evidence evidence.json] [--population 4]');
    process.exit(1);
  }
  const record = await readJsonInput(arg);
  let evidence = {};
  if (evPath) {
    try { evidence = JSON.parse(await readFile(evPath, 'utf8')); }
    catch { console.error('⛔ 证据文件不是合法 JSON'); process.exit(1); }
  }
  const popIdx = process.argv.indexOf('--population');
  const profile = { population: popIdx > 0 ? Number(process.argv[popIdx + 1]) || 4 : 4 };
  const result = analyze(record, { evidence, profile });
  for (const [type, list] of Object.entries(result.findings)) {
    console.log(`\n「${type}」`);
    for (const x of list) console.log(`  [${x.level.toUpperCase().padEnd(4)}] ${x.title}${x.detail ? ' — ' + x.detail : ''}`);
  }
  console.log(`\n「观点提炼」`);
  console.log(`  事实：${result.viewpoint.fact}`);
  console.log(`  代价：${result.viewpoint.cost}`);
  console.log(`  结论：${result.viewpoint.verdict}`);
  console.log(`\nprovenance: ${result.record.provenance ?? '(未定)'}`);
}

// 真实性验证：AI 采集证据（小区库/在售列表/政府公示），判定表由脚本执行（零 token、可测试）
async function cmdVerify(arg, evPath) {
  if (!arg) {
    console.error('用法: node scripts/scan.mjs verify <record.json> [--evidence evidence.json]');
    process.exit(1);
  }
  const record = await readJsonInput(arg);
  let evidence = {};
  if (evPath) {
    try { evidence = JSON.parse(await readFile(evPath, 'utf8')); }
    catch { console.error('⛔ 证据文件不是合法 JSON'); process.exit(1); }
  } else {
    console.error('ℹ️  未提供 --evidence：只做记录内检查；真实判定需实采证据（小区库/在售列表/政府公示）');
  }
  const result = verifyAuthenticity(record, evidence);
  console.log(JSON.stringify({ provenance_suggestion: result.provenance_suggestion, checks: result.checks }, null, 2));
}

// 实体匹配：新记录 vs data/scans/ 全库——识别跨平台同源挂牌与下架重挂
async function cmdMatch(arg) {
  if (!arg) {
    console.error('用法: node scripts/scan.mjs match <record.json | ->');
    process.exit(1);
  }
  const { record, warnings } = normalizeRecord(await readJsonInput(arg));
  warnings.forEach((w) => console.error(`⚠️  ${w}`));
  const dir = join(ROOT, 'data', 'scans');
  const files = (await readdir(dir).catch(() => [])).filter((f) => f.endsWith('.json'));
  const corpus = [];
  for (const f of files) {
    try {
      corpus.push(JSON.parse(await readFile(join(dir, f), 'utf8')));
    } catch {}
  }
  const { fingerprint, matches } = matchRecord(record, corpus);
  const selfKey = `${record.platform}:${record.listing_id ?? record.url}`;
  const foreign = matches.filter((m) => m.listing_key !== selfKey);
  console.log(JSON.stringify({
    fingerprint,
    note: foreign.some((m) => m.confidence === 'high')
      ? '命中同源挂牌：同一物理房屋的多平台/重挂记录——历史按实体关联，注意对比各键价差'
      : matches.length
        ? '仅低/中置信匹配——人工核对新扫描与旧记录是否同源'
        : '无同源记录（新实体或新房源）',
    matches: foreign,
  }, null, 2));
}

// 政务源查询：parser 与枚举断言见 scripts/lib/official-sources.mjs（scan/doctor/selftest 共用）。
// 多市场：templates/official-sources.<market>.yml 全部参与；--market 既可查表级市场（cn/eu）也可查国别码。
async function cmdOfficial(query, opts = {}) {
  const { files, entries } = await readOfficialSources(ROOT);
  if (!files.length) {
    console.error('⛔ templates/ 下没有 official-sources.*.yml 登记表');
    process.exitCode = 2;
    return;
  }
  const list = filterSources(entries, { query, market: opts.market });
  if (!list.length) {
    const markets = [...new Set(entries.map((e) => e.market))].join(' / ');
    console.log(`未找到「${query ?? '全部'}」${opts.market ? `（市场 ${opts.market}）` : ''}的登记条目。已登记市场：${markets}。
 中国城市：检索「城市名 住建委 / 房地产交易中心」官方平台；
 欧洲：检索各国 land registry / cadastre / 统计局官方域名；
 核实后按 templates/official-sources.<market>.yml 的现有格式补入（带 as_of、verify_before_use 与 tier）。`);
    process.exitCode = 2;
    return;
  }
  console.log(JSON.stringify(list, null, 2));
}

const [cmd, ...rest] = process.argv.slice(2);
const main = { detect: cmdDetect, normalize: cmdNormalize, crosscheck: cmdCrosscheck, official: cmdOfficial, history: cmdHistory, match: cmdMatch, verify: cmdVerify, analyze: cmdAnalyze, evidence: cmdEvidence };
if (!cmd || !main[cmd]) {
  console.error('用法: node scripts/scan.mjs <detect|normalize|crosscheck|official|history|match|verify|analyze|evidence> …（详见本文件头注释与 modes/scan.md）');
  process.exit(1);
}
if (cmd === 'crosscheck') await cmdCrosscheck(rest[0], rest.includes('--write'));
else if (cmd === 'verify') {
  const evIdx = rest.indexOf('--evidence');
  await cmdVerify(rest[0], evIdx >= 0 ? rest[evIdx + 1] : undefined);
}
else if (cmd === 'analyze') {
  const evIdx = rest.indexOf('--evidence');
  await cmdAnalyze(rest[0], evIdx >= 0 ? rest[evIdx + 1] : undefined);
}
else if (cmd === 'evidence') await cmdEvidence(rest);
else if (cmd === 'detect') await cmdDetect(rest);
else if (cmd === 'official') {
  const mi = rest.indexOf('--market');
  await cmdOfficial(rest.find((a) => !a.startsWith('--')), mi >= 0 ? { market: rest[mi + 1] } : {});
}
else await main[cmd](rest.find((a) => !a.startsWith('--')));
