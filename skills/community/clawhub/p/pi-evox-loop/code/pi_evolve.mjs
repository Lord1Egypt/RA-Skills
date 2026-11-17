#!/usr/bin/env node
// v0.12.0 — 默认内置 light 后端（零 npm 依赖）；evolver 为可选集成（--engine evolver）
/**
 * pi_evolve.mjs — Pi × EvoX 闭环编排器
 * 默认本地运行（无外发）、人工审核门默认开启；唯一外发路径 --llm-refine 为显式 opt-in
 * （端点未配置时自动禁用），且与 --auto-approve 组合默认拒绝（需 --allow-unreviewed-refine）。
 *
 * 一条命令跑通：Pi 执行 R1 → 适配器转换 session → evolver ingest --distill（自动起草基因）
 *   → [人工审核门：evolver review --approve] → evolver inject → Pi 执行 R2（注入基因）
 * 并输出跨轮 token / 错误数对比。
 *
 * 用法：
 *   node bin/pi_evolve.mjs <repo模板目录> <任务文本文件> \
 *       --provider agnes-cn --model agnes-2.5-flash \
 *       --api-key "$AGNES_CN_API_KEY" \
 *       --rounds 2 --fresh --auto-approve
 *
 * 关键：
 *   --fresh           运行前备份并清空 ~/.evomap/assets（保证单变量、隔离历史资产）
 *   --auto-approve    跳过人工审核门，自动 review --approve（全自动化演示用）
 *                      默认（不带此 flag）= 在蒸馏出基因后暂停，打印审核命令交人工确认
 *   --root <dir>      工作根目录（默认 exp/loop-<时间戳>）
 */
import { spawnSync } from 'node:child_process';
import { selectEngine } from './engine/index.mjs';
import { isApprovedState } from './engine/light/store.mjs';
// 0.31（S5）：注入守卫。静态导入 —— 编排器不是宿主 bootstrap，模块缺失应当**响亮失败**，
// 不做静默降级（与 evolver-recall 的 try/catch 降级策略不同，那边必须保证宿主能启动）。
import { injectionScan } from './injection_scan.mjs';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const LAB = path.resolve(fileURLToPath(import.meta.url), '..', '..'); // repo root (code/ 的上级)
// 可选：指定 node 所在目录（多版本共存时用，如受管 node）。未设置则用 PATH 中的 node。
const MANAGED_NODE = process.env.PI_NODE_HOME || '';
// 辅助脚本布局自适应：仓库布局为 code/，evolver-lab 本机布局为 adapter/ + exp/
const ADAPTER = fs.existsSync(path.join(LAB, 'code', 'pi_session_adapter.js'))
  ? 'code/pi_session_adapter.js' : 'adapter/pi_session_adapter.js';
const SUMTOK = fs.existsSync(path.join(LAB, 'code', 'sum_tokens.js'))
  ? 'code/sum_tokens.js' : 'exp/sum_tokens.js';
// 与 engine/light/store.mjs 保持一致：支持 EVO_STORE_DIR 覆盖（测试隔离 / 多库切换）
const EVO_STORE = process.env.EVO_STORE_DIR || path.join(os.homedir(), '.evomap', 'assets');
// --llm-refine 使用的 OpenAI 兼容端点与模型（实验环境实测用 agnes-cn，可替换为任意兼容服务）
const REFINE_URL = process.env.EVOLVER_REFINE_URL || '';  // 必须显式配置（外发端点，防默认数据外发）
const REFINE_MODEL = process.env.EVOLVER_REFINE_MODEL || '';  // 必须显式配置
const EVO_GENES = path.join(EVO_STORE, 'genes.jsonl');
const EVO_REVIEW = path.join(EVO_STORE, 'review.jsonl');

// ---------- 参数解析 ----------
const positional = [];
const opts = { rounds: 2, fresh: false, autoApprove: false };
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a === '--fresh') opts.fresh = true;
  else if (a === '--auto-approve') opts.autoApprove = true;
  else if (a === '--provider') opts.provider = process.argv[++i];
  else if (a === '--model') opts.model = process.argv[++i];
  else if (a === '--api-key') opts.apiKey = process.argv[++i];
  else if (a === '--rounds') opts.rounds = parseInt(process.argv[++i], 10);
  else if (a === '--root') opts.root = process.argv[++i];
  else if (a === '--task') opts.taskText = process.argv[++i];
  else if (a === '--ext-inject') opts.extInject = true;
  else if (a === '--allow-unreviewed-refine') opts.allowUnreviewedRefine = true;
  else if (a === '--engine') opts.engine = process.argv[++i];
  else if (a === '--strategy-format') opts.strategyFormat = process.argv[++i];
  else if (a === '--arm') opts.arm = process.argv[++i]; // 0.23 U1: targeted(默认) | full-context（长上下文灌库基线臂）
  else if (a === '--llm-refine') opts.llmRefine = true;
  else positional.push(a);
}
const templateDir = positional[0];
const taskFile = positional[1];
if (!templateDir || (!taskFile && !opts.taskText)) {
  console.error('用法: node bin/pi_evolve.mjs <repo模板目录> <任务文本文件> --provider X --model Y --api-key $K [--rounds 2] [--fresh] [--auto-approve] [--arm targeted|full-context]');
  process.exit(2);
}
const taskText = opts.taskText ?? fs.readFileSync(taskFile, 'utf8').trim();
const apiKey = opts.apiKey ?? process.env.AGNES_CN_API_KEY;
if (opts.autoApprove && opts.llmRefine && !opts.allowUnreviewedRefine) {
  logErr('[安全门] --auto-approve 与 --llm-refine 组合会形成「LLM 重写 → 自动审核 → 注入后续轮次」的未经人工复核链路，默认拒绝执行。');
  logErr('  如确需（研究演示），显式追加 --allow-unreviewed-refine 表示已知悉风险；');
  logErr('  或去掉 --auto-approve，保留人工审核门（默认、推荐）。');
  process.exit(2);
}
if (opts.autoApprove && opts.llmRefine && opts.allowUnreviewedRefine) {
  log('⚠️  [组合放行] --allow-unreviewed-refine 已显式指定：LLM 重写的修法将自动审核并注入后续轮次（研究演示模式，请勿用于生产）。');
}
// provider/model 白名单（防注入：仅允许安全字符集）
for (const [name, v] of [['provider', opts.provider], ['model', opts.model]]) {
  if (v && !/^[A-Za-z0-9._\-]+$/.test(v)) {
    logErr(`[安全门] ${name} 含非法字符（仅允许字母/数字/点/下划线/连字符）`);
    process.exit(2);
  }
}
if (!opts.provider || !opts.model || !apiKey) {
  logErr('缺少 --provider / --model / --api-key（或环境变量 AGNES_CN_API_KEY）');
  process.exit(2);
}

/**
 * 输出脱敏（0.10.0，响应云鼎动态引擎 finding「密钥形态值打印到 stdout」）：
 * log 的所有输出统一做两层掩码——
 *   1) 已注册的敏感值（apiKey 等）整体替换为 ***；
 *   2) 通用 key 形态（sk-xxx / Bearer xxx / 长随机串）模式掩码。
 */
const SENSITIVE_VALUES = new Set();
function registerSecret(v) { if (v && String(v).length >= 8) SENSITIVE_VALUES.add(String(v)); }
function redact(s) {
  let out = String(s);
  for (const v of SENSITIVE_VALUES) out = out.split(v).join('***');
  return out
    .replace(/\b(sk-[A-Za-z0-9_\-]{8,})/g, 'sk-***')
    .replace(/\b(Bearer\s+)[A-Za-z0-9_.\-]{8,}/gi, '$1***');
}
const log = (...x) => console.log(...x.map(redact));
const logErr = (...x) => console.error(...x.map(redact));
// 敏感值注册（须在 SENSITIVE_VALUES 定义之后调用，避免 TDZ；0.11.0 修复 0.10.0 的初始化顺序缺陷）
registerSecret(process.env.AGNES_CN_API_KEY);
registerSecret(process.env.EVOLVER_REFINE_URL);
registerSecret(process.env.DEEPSEEK_API_KEY);

/**
 * CLI 执行 —— argv 化（0.6.0 安全加固，彻底消除 shell 字符串拼接）：
 * 全部以 argv 数组调用 `node <JS 入口>`，不经过 bash/shell，参数不参与任何解析，
 * 从根上消除命令注入面（响应 ClawHub static-analysis: unsafe shell construction）。
 *   PI_ENTRY       → pi 的 CLI 入口（package.json bin 指向 dist/cli.js）
 *   EVOLVER_ENTRY  → evolver 的 CLI 入口
 * 选项语义与旧 shell 版对齐：silent ≈ `2>/dev/null`；mergeStderr ≈ `2>&1`；allowFail ≈ 非零退出不抛。
 */
const PI_ENTRY = 'node_modules/@earendil-works/pi-coding-agent/dist/cli.js';
// evolver CLI 调用已收口到 code/engine/evolver-bridge.mjs（双后端统一接口）
/**
 * 失败分类（0.9.0，响应 skillhub「错误分类粗粒度」4.3 分项）：
 * 从子进程输出识别错误家族，给出**可执行的下一步**，而不是只丢退出码。
 */
const ERROR_HINTS = [
  [/ENOENT|Cannot find module|no such file or directory/i, '依赖/路径类：确认已在仓库根目录执行且 `npm install` 完整（缺件可试 `npm rebuild`）；检查传入的路径是否存在'],
  [/EACCES|EPERM|Permission denied|operation not permitted/i, '权限类：目标文件/目录权限不足（Linux 用 chmod，Windows 检查只读属性）'],
  [/ETIMEDOUT|ENOTFOUND|ECONNREFUSED|ECONNRESET|socket hang up|timeout/i, '网络类：检查连通性与代理设置（HTTP_PROXY/HTTPS_PROXY 可能干扰直连，可 no_proxy 排除）'],
  [/401|403|Unauthorized|invalid api key|无效的令牌|authentication/i, '凭据类：API key 无效或未正确传递（用 --api-key 显式传，或确认环境变量已导出）'],
  [/429|rate limit|too many requests/i, '限流类：稍后重试，或更换模型/端点'],
];
function classifyError(text) {
  for (const [re, hint] of ERROR_HINTS) if (re.test(text)) return hint;
  return null;
}
function runCli(entry, args, { cwd = LAB, silent = false, mergeStderr = false, allowFail = false, extraEnv = null, timeout = Number(process.env.EVOX_CLI_TIMEOUT_MS) || 600000 } = {}) {
  const env = { ...process.env, ...(extraEnv ?? {}) };
  if (MANAGED_NODE) env.PATH = `${MANAGED_NODE}${path.delimiter}${env.PATH ?? ''}`;
  const r = spawnSync(process.execPath, [entry, ...args], { cwd, encoding: 'utf8', maxBuffer: 1 << 26, env, timeout });
  if (r.error) {
    // 超时 / 启动失败：allowFail 调用方（sum_tokens / adapter 等尽力而为）静默返回，其余抛出可读错误。
    // 超时（code=ETIMEDOUT）按网络类诊断提示，并说明可用 EVOX_CLI_TIMEOUT_MS 调整上限。
    if (allowFail) return '';
    const code = r.error.code || 'error';
    const hint = classifyError(code === 'ETIMEDOUT'
      ? 'ETIMEDOUT 子进程超时（可用环境变量 EVOX_CLI_TIMEOUT_MS 调大上限，单位毫秒，默认 600000）'
      : code);
    const err = new Error(`子进程调用失败（${code}）：${String(r.error.message).slice(0, 200)}${hint ? `\n  ↳ 诊断：${hint}` : ''}`);
    err.code = code;
    throw err;
  }
  const out = (r.stdout ?? '') + (mergeStderr ? (r.stderr ?? '') : '');
  if (!allowFail && r.status !== 0) {
    const detail = String(r.stderr ?? '').trim().slice(0, 200);
    const hint = classifyError(`${detail} ${out}`);
    const err = new Error(`exit ${r.status}: ${detail}${hint ? `\n  ↳ 诊断：${hint}` : ''}`);
    err.status = r.status;
    err.hint = hint;
    throw err;
  }
  return out;
}
function globJsonl(dir) {
  try { return fs.readdirSync(dir).filter((f) => f.endsWith('.jsonl')); } catch { return []; }
}

/**
 * 注入质量守卫：strategy 须命中「修法信号词」。
 * 规则已在 4 个真实历史样本上验证（§16 gbk修法✓ / §17 容错修法✓ / §20 成功总结✗ / §18 gb18030叙述✓）。
 */
const REPAIR_SIGNAL_RE = /error|exception|traceback|failed|invalid|cannot|unable|missing|not found|wrong|instead|avoid|fix|encoding\s*[=:]|errors\s*=|utf-?8|gbk|gb18030|latin-1|\brb\b|except|skip|avoid\s*:|fix\s*:/i;
const isRepairLike = (t) => REPAIR_SIGNAL_RE.test(t);

/**
 * 从 ~/.evomap/assets/genes.jsonl 抽取已审核（approved）基因的 strategy 文本。
 * evolver inject session-start 只输出 summary 标签，不携带可执行修法；
 * 这里直接读基因库把 strategy 拼回注入块，让下一轮真正继承"怎么做"而非仅"出过什么错"。
 * 审核态以 review.jsonl 中 asset_id 对应的 approved 记录为准（尊重人工/自动审核门）。
 */
function loadApprovedStrategy() {
  try {
    // 1) 收集已 approved 的 asset_id 集合
    //    追加式台账 ⇒ 以「每个 assetId 的最后一条状态」为准（last-write-wins）；
    //    否则 quarantine 无法撤销已批准，被隔离的基因仍会被注入。
    //    修复（2026-09-23）：与 evolver-recall.mjs / evolver-bridge.ts 的 2026-09-17 修复对齐（此前遗漏本处）。
    const latestState = new Map();
    try {
      for (const line of fs.readFileSync(EVO_REVIEW, 'utf8').split('\n')) {
        const s = line.trim();
        if (!s) continue;
        try {
          const r = JSON.parse(s);
          if (r && typeof r.assetId === 'string' && r.assetId) latestState.set(r.assetId, r.state);
        } catch {}
      }
    } catch {}
    const approved = new Set();
    for (const [assetId, state] of latestState) {
      // 0.31 安全修复：精确比对（旧写法 `includes('approv')` 会放行 unapproved/disapproved）。
      if (isApprovedState(state)) approved.add(assetId);
    }
    // 2) 抽取这些基因的 strategy
    const out = [];
    for (const line of fs.readFileSync(EVO_GENES, 'utf8').split('\n')) {
      const s = line.trim();
      if (!s) continue;
      let g;
      try { g = JSON.parse(s); } catch { continue; }
      const st = g && g.strategy;
      if (!Array.isArray(st) || !st.length) continue;
      const aid = g.asset_id;
      // fail-closed（安全修复 0.6.0，ClawHub clawscan 二次点名）：台账缺失/为空或未 approved → 一律跳过。
      // 旧逻辑 "approved.size &&" 在台账不可用时退化为全采纳（fail-open），违背审核门语义。
      if (!aid || !approved.has(aid)) continue;
      const text = st.join(' ').slice(0, 1200);
      if (!isRepairLike(text)) continue; // 守卫：无修法信号的叙述（如成功总结）不注入，宁缺毋滥（§20）
      // 0.31 注入守卫（S5）：与 evolver-recall 同口径——文档声称注入守卫覆盖「召回」，
      // 而编排器是另一条注入通道，此前缺位（ClawHub clawscan 点名）。
      if (!injectionScan(g).ok) continue;
      out.push(`- [${g.category || 'repair'}] ${text}`);
    }
    return out.join('\n\n').slice(0, 4000);
  } catch { return ''; }
}

// ---------- 实验环境自检（preflight，0.14.6 P3a，回应 skillhub stability 4.4「环境配错难排查」）----------
// 流程 C 启动前校验 Node / pi 版本 / 可选 evolver 后端 / 经验库可写，配错时打印明确诊断而非静默失败。
function preflight() {
  const checks = [];
  const nodeMajor = Number(process.versions.node.split('.')[0]);
  checks.push({ name: 'Node ≥22', ok: nodeMajor >= 22, detail: `v${process.versions.node}`, fix: '升级到 Node ≥22 后重试（pi/evolver 与 traps 均要求）' });
  const piPkgPath = path.join(LAB, 'node_modules', '@earendil-works', 'pi-coding-agent', 'package.json');
  if (fs.existsSync(piPkgPath)) {
    try {
      const v = JSON.parse(fs.readFileSync(piPkgPath, 'utf8')).version || '0.0.0';
      const [maj, min, pat] = v.split('.').map((n) => parseInt(n, 10) || 0);
      const ok = maj > 0 || min > 85 || (min === 85 && pat >= 1);
      checks.push({ name: 'pi ≥0.85.1（支持 $ENV 插值）', ok, detail: `v${v}`, fix: '升级 pi-coding-agent ≥0.85.1；否则 models.json 的 $ENV 插值需改用 --api-key 显式传（见 FAQ·Q2）' });
    } catch { checks.push({ name: 'pi 版本可解析', ok: false, detail: 'package.json 解析失败', fix: '重新 npm install' }); }
  } else {
    checks.push({ name: 'pi 已安装', ok: false, detail: 'node_modules/@earendil-works/pi-coding-agent 缺失', fix: '先在仓库根目录执行 npm install' });
  }
  if (opts.engine === 'evolver') {
    const evoOk = fs.existsSync(path.join(LAB, 'node_modules', '@evomap', 'evolver', 'bin', 'evolver.js'));
    checks.push({ name: 'evolver 后端已安装（--engine evolver）', ok: evoOk, detail: evoOk ? '已就位' : '缺失', fix: 'npm install 安装 @evomap/evolver（GPL，可选集成）' });
  }
  let storeOk = true, storeDetail = EVO_STORE;
  try {
    fs.mkdirSync(EVO_STORE, { recursive: true });
    const probe = path.join(EVO_STORE, '.pi-evox-pf');
    fs.writeFileSync(probe, 'ok'); fs.rmSync(probe, { force: true });
  } catch (e) { storeOk = false; storeDetail = `${EVO_STORE} 不可写：${String(e.message).slice(0, 80)}`; }
  checks.push({ name: '经验库目录可写', ok: storeOk, detail: storeDetail, fix: '检查目录权限 / 杀软拦截' });
  log('=== 实验环境自检（preflight） ===');
  let fail = 0;
  for (const c of checks) {
    log(`  [${c.ok ? '✓' : '✗'}] ${c.name} —— ${c.detail}`);
    if (!c.ok) { log(`      → 修正：${c.fix}`); fail++; }
  }
  if (fail) { logErr(`\npreflight 未通过 ${fail} 项，请修正后再跑流程 C 实验（日常 A/B 流程不受影响）。`); process.exit(2); }
  log('✓ 实验环境就绪。');
}

// ---------- 工作区 ----------
preflight();
const root = opts.root ?? path.join(LAB, 'exp', `loop-${Date.now()}`);
fs.mkdirSync(root, { recursive: true });
fs.writeFileSync(path.join(root, 'task.txt'), taskText);
const sessBase = path.join(root, 'sessions');

// ---------- 可选：清空资产库（单变量控制）----------
if (opts.fresh) {
  const bk = path.join(EVO_STORE, `backup-${Date.now()}`);
  fs.mkdirSync(bk, { recursive: true });
  // 全新环境兼容：~/.evomap/assets 尚未初始化（文件不存在）时以空库起步，不报 ENOENT
  for (const [src, name] of [[EVO_GENES, 'genes.jsonl'], [EVO_REVIEW, 'review.jsonl']]) {
    if (fs.existsSync(src)) fs.copyFileSync(src, path.join(bk, name));
    fs.writeFileSync(src, '');
  }
  log(`[fresh] 已备份旧资产库到 ${bk} 并清空（${fs.existsSync(path.join(bk, 'genes.jsonl')) ? '含旧资产' : '原为空库'}）`);
}

// ---------- 引擎选择（0.12.0：默认内置 light 后端）----------
// 默认 light（纯 Node 内置模块，零 npm 依赖）；--engine evolver 可用可选集成；--engine auto 为旧行为。
// 存储格式两后端一致（schema 1.13.0），产物可互操作。
const engine = selectEngine(opts.engine ?? 'light', { root: LAB, log });
log(`[engine] 使用后端：${engine.name}`);

// ---------- 预置陷阱内容到 LAB 根（泛化：模板目录的全部顶层条目）----------
// 0.8.0：不再写死 data/events.jsonl——支持多种陷阱形态（脚本行尾 / 只读文件 / NFD 文件名等）。
// 安全（ClawHub environment_proportionality concern）：记录运行前既有条目，cleanup 只删本轮预置的；
// 若 LAB 根已存在同名条目则跳过预置（绝不覆盖既有文件）。
const preExistingLabArtifacts = {};
const stagedEntries = [];
try {
  for (const entry of fs.readdirSync(templateDir)) {
    preExistingLabArtifacts[entry] = fs.existsSync(path.join(LAB, entry));
    if (preExistingLabArtifacts[entry]) {
      log(`[stage] 跳过 ${entry}（LAB 根已存在同名条目，不覆盖）`);
      continue;
    }
    fs.cpSync(path.join(templateDir, entry), path.join(LAB, entry), { recursive: true });
    stagedEntries.push(entry);
  }
  if (stagedEntries.length) log(`[stage] 已预置模板内容到 LAB 根: ${stagedEntries.join(', ')}`);
} catch (e) { log(`[stage] 预置失败: ${String(e).slice(0, 120)}`); }

// ---------- 主循环 ----------
const results = [];
const labRootRel = LAB;

for (let r = 1; r <= opts.rounds; r++) {
  const work = path.join(root, `r${r}`);
  fs.rmSync(work, { recursive: true, force: true });
  fs.cpSync(templateDir, work, { recursive: true });
  const sessDir = path.join(sessBase, `r${r}`);
  fs.mkdirSync(sessDir, { recursive: true });

  // 注入块（R>1 时读取已审核基因）
  // 单通道原则：若 Pi 扩展桥已激活（.pi/extensions/evolver-bridge.ts 存在），
  // 自动走扩展注入并跳过 CLI 策略注入——双通道会把同一修法注入两遍（token 膨胀 + 行为扰动）。
  const extBridgeActive = fs.existsSync(path.join(LAB, '.pi', 'extensions', 'evolver-bridge.ts'));
  let injectArgs = [];
  if (r > 1 && (opts.extInject || extBridgeActive)) {
    // Route A 模式：不传 CLI 注入参数，由 Pi 扩展（.pi/extensions/evolver-bridge.ts）
    // 在 before_agent_start 钩子自动注入已审核基因 strategy；留痕见 ~/.evomap/assets/bridge-last-inject.txt
    log(`[inject] R${r} 使用 Pi 扩展注入（${opts.extInject ? '--ext-inject' : '自动检测：扩展桥已激活'}），跳过 CLI append-system-prompt 以避免双通道重复注入`);
  } else if (r > 1) {
    const block = engine.injectBlock();
    // 关键修复：evolver inject 只吐基因的 summary 标签（如 "bash, exception"），
    // 不携带真正可执行的 strategy（例如 "用 encoding='gbk' 读取"）。这里从 genes.jsonl
    // 抽取已审核基因的 strategy 文本，追加进注入块，使下一轮真正继承"修法"而非仅一个标签。
    let strat;
    if (opts.arm === 'full-context') {
      // 0.23 U1：长上下文灌库基线臂——注入**全部**已审核基因的完整 strategy（不做对靶筛选）。
      // 方法学依据：AMA-Bench 类工作显示长上下文基线必须作为对照臂，否则效果声明不可信。
      const latest = new Map();
      try { for (const line of fs.readFileSync(EVO_REVIEW, 'utf8').split('\n')) { const t = line.trim(); if (!t) continue; try { const rr = JSON.parse(t); if (rr && typeof rr.assetId === 'string' && rr.assetId) latest.set(rr.assetId, rr.state); } catch {} } } catch {}
      // 0.31 安全修复：精确比对（旧写法 `includes('approv')` 会放行 unapproved/disapproved）。
      const ok = new Set([...latest].filter(([, st]) => isApprovedState(st)).map(([aid]) => aid));
      const all = [];
      for (const line of fs.readFileSync(EVO_GENES, 'utf8').split('\n')) {
        const t = line.trim(); if (!t) continue;
        let g; try { g = JSON.parse(t); } catch { continue; }
        if (!g.asset_id || !ok.has(g.asset_id)) continue;
        const st = g.strategy; if (!Array.isArray(st) || !st.length) continue;
        // 0.31（S5）：full-context 臂同样过注入守卫 —— 该臂本就是「不做对靶筛选」的长上下文对照臂，
        // 「不做对靶筛选」不等于「不做安全检查」。
        if (!injectionScan(g).ok) continue;
        all.push(`- [${g.category || 'repair'}] ${st.join(' ').slice(0, 1200)}`);
      }
      strat = all.join('\n');
      log(`[inject] R${r} 臂=full-context：灌入全部 ${all.length} 条已审核基因（无对靶筛选）`);
    } else {
      strat = loadApprovedStrategy();
    }
    const full = strat
      ? `${block}\n\n[上一轮已验证的修法（请优先采用，避免重复踩坑）]\n${strat}`
      : block;
    const f = path.join(root, `inject-r${r}.txt`);
    fs.writeFileSync(f, full);
    injectArgs = ['--append-system-prompt', full]; // argv 直传内容，无需 shell 命令替换
  }

  log(`\n========== ROUND ${r} ${r > 1 ? '(injected)' : '(baseline)'} ==========`);
  const taskF = path.join(root, `task-r${r}.txt`);
  fs.writeFileSync(taskF, taskText);
  const piArgs = ['-p', '--provider', opts.provider, '--model', opts.model,
    '--api-key', apiKey, '--session-dir', sessDir, ...injectArgs, taskText];
  let piOut = '';
  try {
    piOut = runCli(PI_ENTRY, piArgs, { mergeStderr: true, extraEnv: { AGNES_CN_API_KEY: apiKey } });
    log(piOut.trim().split('\n').slice(-8).join('\n')); // 仅尾部摘要，避免刷屏
  } catch (e) {
    log(`[round ${r}] pi 运行异常: ${String(e).slice(0, 300)}`);
  }

  // 聚合 token
  let stats = null;
  try {
    const out = runCli(SUMTOK, [sessDir], { silent: true });
    stats = JSON.parse(out);
  } catch (e) { log(`[round ${r}] sum_tokens 失败: ${String(e).slice(0, 200)}`); }
  // 0.13.0：injected 记录**实际是否注入了非空策略**（原先仅 r>1，会把"无基因可注入"误记为已注入）
  const实际注入 = r > 1 && (injectArgs.length > 0 || (opts.extInject || extBridgeActive));
  results.push({ round: r, injected: 实际注入, stats });

  // R1 之后：转换 + 蒸馏
  if (r === 1 && opts.rounds > 1) {
    const sessFiles = globJsonl(sessDir);
    if (sessFiles.length) {
      const sf = path.join(sessDir, sessFiles[0]);
      const outDir = path.join(root, 'transcript');
      fs.mkdirSync(outDir, { recursive: true });
      try {
        runCli(ADAPTER, [sf, '--out', outDir, '--active-only'], { silent: true });
      } catch (e) {
        log(`[adapter] 转换失败，跳过本轮蒸馏: ${String(e).slice(0, 150)}`);
      }
      const tr = globJsonl(outDir).find((f) => f.endsWith('.transcript.jsonl'));
      if (tr) {
        const ingestRes = engine.ingestDistill(path.join(outDir, tr), { strategyFormat: opts.strategyFormat ?? 'narrative' });
        const ingestOut = ingestRes.raw;
        log(`[distill] ${ingestOut.trim().split('\n').slice(-4).join('\n')}`);
        // 直接用 engine 返回的 geneId（两后端统一契约）——不再依赖对 CLI 输出文本的正则解析
        if (ingestRes.geneId) {
          const gene = ingestRes.geneId;
          if (opts.autoApprove) {
            engine.approve(gene);
            log(`[gate] 自动审核通过 ${gene}（--auto-approve）`);
          } else {
            log(`\n🔒 人工审核门：请审阅后执行\n  node_modules/.bin/evolver review --approve ${gene}\n（通过后将注入下一轮）`);
            // 默认不自动 approve：这里仍继续跑 R2，但 R2 不会注入（store 无已审核基因）
          }
        } else {
          log('[distill] 本轮未自动起草基因（无 strong 信号或去重拦截）；R2 将作为无注入基线重复。');
        }

        // ---------- --llm-refine：守卫判 strategy 无修法 → LLM 重写 → manual distill ----------
        if (opts.llmRefine) {
          const stratRaw = loadApprovedStrategy();
          if (!stratRaw) {
            log('[llm-refine] store 无已审核 strategy，跳过重写');
          } else if (isRepairLike(stratRaw)) {
            log('[llm-refine] strategy 已含修法信号词，无需重写');
          } else if (!REFINE_URL || !REFINE_MODEL) {
            // 数据外发端点必须显式配置（SkillSpector finding 修复：不做默认外发）
            log('[llm-refine] strategy 无修法信号，但未配置 EVOLVER_REFINE_URL / EVOLVER_REFINE_MODEL（外发端点必须显式指定），跳过重写');
          } else {
            log('[llm-refine] strategy 无修法信号（成功总结型叙述）→ LLM 重写');
            const trTxt = fs.readFileSync(path.join(outDir, tr), 'utf8').replace(/\s+/g, ' ').slice(0, 9000);
            const prompt =
              'Below is an agent coding-session transcript. The agent hit errors and recovered. ' +
              'Extract the CONCRETE FIX as ONE single-line strategy (steps separated by "; "). ' +
              'Focus on what caused the error and the exact code/config change that resolved it. ' +
              'Output ONLY the strategy sentence, no preamble, no markdown.\n\nTRANSCRIPT:\n' + trTxt;
            const pf = path.join(root, 'llm-prompt.txt');
            const rf = path.join(root, 'llm-response.txt');
            fs.writeFileSync(pf, prompt);
            const pfP = pf.replace(/\\/g, '/'), rfP = rf.replace(/\\/g, '/');
            try {
              // 0.6.0：curl → Node 原生 fetch（消除 shell/curl 依赖，外发目标与载荷在代码中显式可见）
              const resp = await fetch(REFINE_URL, {
                method: 'POST',
                headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: REFINE_MODEL, messages: [{ role: 'user', content: prompt }], max_tokens: 300 }),
                signal: AbortSignal.timeout(180000),
              });
              const respJson = await resp.json().catch(() => null);
              const refined = String(respJson?.choices?.[0]?.message?.content ?? '').trim();
              fs.writeFileSync(rf, refined);

              if (refined && isRepairLike(refined)) {
                const oneLine = refined.replace(/\r?\n+/g, ' ').replace(/"/g, "'");
                const dmRes = engine.distillManual({
                  category: 'repair', signals: 'read,bash,exception',
                  strategy: oneLine, summary: 'LLM-refined repair (guard-triggered)',
                });
                const dOut = dmRes.raw;
                log(`[llm-refine] LLM 精修 strategy 已蒸馏: ${dOut.trim().split('\n').slice(-2).join(' | ').slice(0, 200)}`);
                const gmId = dmRes.geneId;
                if (gmId && opts.autoApprove) {
                  engine.approve(gmId);
                  log(`[llm-refine] 已自动审核通过 ${gmId}（--auto-approve）`);
                } else if (gmId) {
                  log(`[llm-refine] 人工审核门：evolver review --approve ${gmId}  （或 light 后端：直接审阅 {store}/review.jsonl）`);
                }
              } else {
                log('[llm-refine] LLM 输出为空或仍无修法信号，保留原状（守卫兜底：不注入噪声）');
              }
            } catch (e) {
              log(`[llm-refine] 失败: ${String(e).slice(0, 200)}`);
            }
          }
        }
      }
    }
  }
}

// ---------- 对比表 ----------
log('\n================ 跨轮对比 ================');
log('round | injected | totalTokens | input | output | toolCalls | errors');
for (const res of results) {
  const u = res.stats?.usage ?? {};
  log(`${String(res.round).padEnd(5)} | ${String(res.injected).padEnd(8)} | ${String(u.totalTokens ?? '-').padEnd(12)} | ${String(u.input ?? '-').padEnd(5)} | ${String(u.output ?? '-').padEnd(6)} | ${String(res.stats?.toolCalls ?? '-').padEnd(9)} | ${res.stats?.toolErrors ?? '-'}`);
}
if (results.length >= 2) {
  const b = results[0].stats?.usage?.totalTokens, a = results[results.length - 1].stats?.usage?.totalTokens;
  if (b && a) log(`\n基线首轮 ${b} → 末轮 ${a}（Δ ${(((a - b) / b) * 100).toFixed(1)}%）`);
}
log(`\n工作区: ${root}`);

// ---------- 清理 LAB 临时产物（仅删本轮预置的、且运行前不存在的条目）----------
let cleaned = 0, kept = 0;
for (const entry of stagedEntries) {
  const p = path.join(LAB, entry);
  if (preExistingLabArtifacts[entry]) { kept++; log(`[cleanup] 保留 ${p}（运行前已存在）`); continue; }
  try { fs.rmSync(p, { recursive: true, force: true }); cleaned++; } catch {}
}
// Pi 在 LAB 根新建的常见产物（仅当运行前不存在时清理）
for (const extra of ['analyze.py']) {
  const p = path.join(LAB, extra);
  if (!fs.existsSync(p) || preExistingLabArtifacts[extra]) continue;
  try { fs.rmSync(p, { force: true }); cleaned++; } catch {}
}
log(`[cleanup] 已清理 LAB 临时产物（删除 ${cleaned} 项，保留 ${kept} 项）`);
