/**
 * engine/light/store.mjs — 轻量后端的存储层
 *
 * 与 Evolver 资产库格式**完全兼容**（schema 1.13.0）：
 *   ~/.evomap/assets/genes.jsonl   —— 基因（每行一个 Gene）
 *   ~/.evomap/assets/review.jsonl  —— 审核台账（每行 {assetId, state, reason, at}）
 *
 * 设计约定：
 * - 后端可互换：本模块写入的记录，evolver 后端可直接读取（反之亦然）；
 * - 容错：坏行跳过（不因单行损坏导致整体不可读）；
 * - 库路径可用 EVO_STORE_DIR 覆盖（测试/隔离用）。
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const STORE_DIR = process.env.EVO_STORE_DIR || path.join(os.homedir(), '.evomap', 'assets');
export const GENES_PATH = path.join(STORE_DIR, 'genes.jsonl');
export const REVIEW_PATH = path.join(STORE_DIR, 'review.jsonl');

/** 读取 JSONL（坏行静默跳过；文件不存在返回空数组） */
const WARNED_MISSING = new Set();
export function readJsonl(p, { warn = false } = {}) {
  const out = [];
  let raw = '';
  try { raw = retryIo(() => fs.readFileSync(p, 'utf8'), 'readJsonl'); } catch {
    // 0.22（0.21.0 评测 errorHandling 点名"文件不存在场景静默返回空数组"）：
    // 区分「空库」与「文件缺失」——CLI 路径（info/timeline/evidence/list）传 warn:true 告警一次；
    // 热路径（approvedAssetIds 等内部调用）保持静默，避免刷屏。
    if (warn && !WARNED_MISSING.has(p)) { WARNED_MISSING.add(p); console.warn(`[pi-evox] 提示：账本文件不存在（${p}）——按空处理；首次沉淀/召回后自动创建`); }
    return out;
  }
  const bad = [];
  let lineNo = 0;
  for (const line of raw.split('\n')) {
    lineNo++;
    const s = line.trim();
    if (!s) continue;
    try { out.push(JSON.parse(s)); } catch { bad.push({ n: lineNo, s: s.slice(0, 80) }); }
  }
  if (warn && bad.length) console.warn(`[pi-evox] 提示：${p} 有 ${bad.length} 行无法解析（已跳过）：行 ${bad.map((b) => b.n).join(', ')}；首条预览: ${bad[0].s}（0.23：手工编辑后请校验 JSON 格式）`);
  return out;
}

// 0.24 场景受控词表（治理/拉取/策展用；召回对靶仍走 signals_match 自由信号）
export const SCENES = ['ops-deploy', 'coding-debug', 'release-publish', 'api-integration', 'git-workflow', 'agent-runtime'];

// 0.25：timeline deposit 事件（沉淀动作可审计——修 B4：draft/distill 落库不产生任何 timeline 事件的缺口）
// 0.26.1 修复：本文件在 code/engine/light/ 下——两级 dirname 只到 code/engine，需四级到技能根。
const HITS_DIR = process.env.EVOX_HITS_DIR || path.join(path.dirname(path.dirname(path.dirname(path.dirname(fileURLToPath(import.meta.url))))), 'experiments');
export function appendDeposit(evt) {
  try {
    fs.mkdirSync(HITS_DIR, { recursive: true });
    fs.appendFileSync(path.join(HITS_DIR, 'deposits.jsonl'), JSON.stringify({ ts: new Date().toISOString(), kind: 'deposit', ...evt }) + '\n');
    return true;
  } catch { return false; }
}
export function readDeposits() { return readJsonl(path.join(HITS_DIR, 'deposits.jsonl'), { warn: false }); }

export const readGenes = () => readJsonl(GENES_PATH);
export const readReview = () => readJsonl(REVIEW_PATH);

function ensureDir() {
  try { fs.mkdirSync(STORE_DIR, { recursive: true }); } catch { /* 已存在 */ }
}

/**
 * 0.21 稳定性：瞬态 IO 错误重试 + 硬截止（stability 评测 0.19.1/0.20.3 两轮点名
 * 「未见显式重试逻辑和超时控制」）。
 * 边界纪律（与 fail-open 哲学一致）：
 *   - 只重试**瞬态**错误（EBUSY/EPERM/EACCES/ETIMEDOUT——Windows 上文件被占用/杀软扫描的典型表现）；
 *   - 总截止 RETRY_DEADLINE_MS（默认 3s）内有限次重试（RETRY_MAX 次），**到点即放行**：
 *     重试是优化不是门——绝不让 IO 因重试机制无限期阻塞调用方；
 *   - 非瞬态错误（ENOENT/EISDIR 等）立即交还原逻辑，不重试。
 *
 * 0.34 熔断/降级（stability 评测 0.33.0 点名「缺少熔断/降级机制，长时间故障时可能持续重试」）：
 *   - 连续 CB_THRESHOLD 次**瞬态**失败 ⇒ 打开熔断：其后 CB_COOLDOWN_MS 内**只尝试 1 次**
 *     （跳过重试与退避），失败即交还调用方 ⇒ 长时间故障下不再无谓重试、响应不被拖慢；
 *   - 冷却期内任一次成功 ⇒ 立即闭合（半开试探自动恢复）；
 *   - 非瞬态失败（ENOENT 等，首次运行的空库场景）**不计入熔断**，避免误触发；
 *   - 打开时输出一次中文可执行指引（限频，不刷屏）。
 */
const RETRY_MAX = Math.max(1, parseInt(process.env.EVOX_IO_RETRY || '3', 10) || 3);
const RETRY_DEADLINE_MS = Math.max(0, parseInt(process.env.EVOX_IO_DEADLINE_MS || '3000', 10) || 3000);
const TRANSIENT = new Set(['EBUSY', 'EPERM', 'EACCES', 'ETIMEDOUT']);
const CB_THRESHOLD = Math.max(2, parseInt(process.env.EVOX_IO_CB_THRESHOLD || '5', 10) || 5);
const CB_COOLDOWN_MS = Math.max(0, parseInt(process.env.EVOX_IO_CB_COOLDOWN_MS || '10000', 10) || 10000);

let cbFailures = 0;
let cbOpenUntil = 0;
let cbGuidanceShown = false;

/** 记录瞬态失败；达到阈值则打开熔断并输出一次可执行指引（非瞬态不计，避免误熔断） */
function noteIoFailure(e) {
  const code = e && e.code;
  if (!TRANSIENT.has(code)) return;
  cbFailures++;
  if (cbFailures >= CB_THRESHOLD) {
    cbOpenUntil = Date.now() + CB_COOLDOWN_MS;
    if (!cbGuidanceShown) {
      cbGuidanceShown = true;
      console.warn(
        `[pi-evox] IO 持续失败（${code}）——已停止重试以保障响应速度（连续 ${CB_THRESHOLD} 次失败触发熔断，冷却 ${CB_COOLDOWN_MS}ms）。` +
        `可执行指引：确认目标文件未被其他程序占用（编辑器/实时扫描），或检查读写权限（EPERM/EACCES）；若存放在网络盘或同步盘，等待同步结束后再试。`
      );
    }
  }
}

export function retryIo(fn, label = 'io') {
  // 熔断打开 ⇒ 降级路径：单次尝试、不重试、不退避（快速失败）
  if (Date.now() < cbOpenUntil) {
    try {
      const r = fn();
      cbFailures = 0; cbOpenUntil = 0; cbGuidanceShown = false; // 半开试探成功 ⇒ 闭合
      return r;
    } catch (e) {
      noteIoFailure(e);
      throw e;
    }
  }
  const start = Date.now();
  for (let attempt = 1; ; attempt++) {
    try {
      const r = fn();
      cbFailures = 0; cbOpenUntil = 0; cbGuidanceShown = false; // 成功 ⇒ 闭合
      return r;
    } catch (e) {
      const code = e && e.code;
      const outOfTime = Date.now() - start >= RETRY_DEADLINE_MS;
      if (!TRANSIENT.has(code) || outOfTime || attempt >= RETRY_MAX) {
        noteIoFailure(e);
        throw e;
      }
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 50 * attempt); // 50/100ms 退避
    }
  }
}

/**
 * 0.19 并发写锁（2026-10-13 第 7 次并发实证后落地）：
 * 多会话/多进程并行写同一 JSONL 台账时，append 之间隔着「读-改-写」窗口会被并发回滚
 * （实测 shareable 标记毫秒级丢失、approve 假 ✓、池计数矛盾）。
 *
 * 协议：O_EXCL 创建 <dir>/.evox.lock（POSIX 与 Windows 均原子）——拿不到则 25ms 轮询；
 *   - stale 破除：锁文件 mtime 超过 LOCK_STALE_MS 视为死锁，可夺取（防持锁进程崩溃）；
 *   - 超时 fail-open：超过 LOCK_TIMEOUT_MS 放弃锁继续执行——**锁是优化不是门**，
 *     任何情况下都不能因锁让写入失败（fail-closed 的反面：这里 fail-open 保可用）。
 * Python 侧（evox_errcap.py hook）用同一协议（os.open O_CREAT|O_EXCL）。
 */
const LOCK_TIMEOUT_MS = Math.max(0, parseInt(process.env.EVOX_LOCK_TIMEOUT_MS || '5000', 10) || 5000);
const LOCK_STALE_MS = 15000;

// 0.34 P1-3 单写者告警：锁的 fail-open 原先**完全静默**（评测点名"缺分布式锁"的可见性缺口）。
// 锁仍然 fail-open（可用性优先，绝不因锁让写入失败），但**必须显式告知**本次未持锁——
// 否则并发写造成的更新丢失对用户是完全不可见的。
let lastLockFailReason = '';
const lockWarned = new Set(); // 按目录限频一次，避免每次写入刷屏

function acquireLock(dir) {
  const lockPath = path.join(dir, '.evox.lock');
  try { fs.mkdirSync(dir, { recursive: true }); } catch { /* 已存在 */ }
  const start = Date.now();
  for (;;) {
    try {
      const fd = fs.openSync(lockPath, 'wx'); // O_EXCL：原子创建，已存在则 EEXIST
      try { fs.writeSync(fd, String(process.pid)); } catch { /* 内容仅诊断用 */ }
      fs.closeSync(fd);
      return lockPath;
    } catch (e) {
      if (e && e.code !== 'EEXIST') { lastLockFailReason = '锁文件无法创建（目录只读或权限不足）'; return null; }
      try {
        const st = fs.statSync(lockPath);
        if (Date.now() - st.mtimeMs > LOCK_STALE_MS) { try { fs.unlinkSync(lockPath); } catch { /* 他人先夺 */ } continue; }
      } catch { continue; } // 锁刚好消失 → 重试
      if (Date.now() - start > LOCK_TIMEOUT_MS) { lastLockFailReason = `等待写锁超过 ${LOCK_TIMEOUT_MS}ms（可能有其他进程正在写）`; return null; }
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 25); // 同步睡眠 25ms
    }
  }
}

function releaseLock(lockPath) {
  if (!lockPath) return;
  try { fs.unlinkSync(lockPath); } catch { /* 已被 stale 夺取者删除 */ }
}

/** 持锁执行 fn（返回 fn 的返回值）；锁不可用时退化为直接执行（fail-open），但会告警一次 */
export function withLock(dir, fn) {
  lastLockFailReason = '';
  const lp = acquireLock(dir);
  if (!lp && !lockWarned.has(dir)) {
    lockWarned.add(dir);
    console.warn(
      `[pi-evox] 警告：本次写入未取得写锁（${lastLockFailReason || '锁不可用'}）——` +
      `若多进程或多机器并发写同一个经验库，可能出现更新丢失（台账回滚、标记丢失）。` +
      `可执行指引：确保同一库只由单个写入者写入；或设 EVOX_LOCK_TIMEOUT_MS 调整等待上限。`
    );
  }
  try { return fn(); } finally { releaseLock(lp); }
}

/** 追加一条基因；asset_id 已存在则跳过（去重）。返回 true=已写入 */
export function appendGene(gene) {
  ensureDir();
  return withLock(STORE_DIR, () => {
    const exists = readGenes().some((g) => g.asset_id && g.asset_id === gene.asset_id);
    if (exists) return false;
    retryIo(() => fs.appendFileSync(GENES_PATH, JSON.stringify(gene) + '\n'), 'appendGene');
    return true;
  });
}

/** 追加审核台账记录 */
export function appendReview(rec) {
  ensureDir();
  return withLock(STORE_DIR, () => {
    const entry = { assetId: rec.assetId, state: rec.state, reason: rec.reason ?? '', at: new Date().toISOString() };
    retryIo(() => fs.appendFileSync(REVIEW_PATH, JSON.stringify(entry) + '\n'), 'appendReview');
    return entry;
  });
}

/**
 * 审核态判定：**唯一权威入口**（0.31 新增）。
 *
 * 为什么必须由一处统一判定：旧写法散落各处做 `state.toLowerCase().includes('approv')`，
 * 而 `'unapproved'` / `'disapproved'` 同样包含子串 'approv' ⇒ **被明确撤销/拒绝的基因
 * 会被当成已批准**，进而注入 system prompt 或进入共享池（ClawHub clawscan + skillspector
 * 于 0.30.0 上点名，实测确认）。
 *
 * 语义：仅 `approved` 为真；大小写/空白归一；**未知或畸形状态一律 false（fail-closed）**。
 */
export function isApprovedState(state) {
  if (typeof state !== 'string') return false;
  return state.trim().toLowerCase() === 'approved';
}

/** 隔离态判定（同上，精确比对）。'unquarantined' 之类不得被算作隔离。 */
export function isQuarantinedState(state) {
  if (typeof state !== 'string') return false;
  return state.trim().toLowerCase() === 'quarantined';
}

/** 已 approved 的 asset_id 集合（fail-closed：台账不可用时为空集，调用方据此跳过注入）
 *  追加式台账 ⇒ 以「每个 assetId 的最后一条状态」为准（last-write-wins）。
 *  修复（2026-09-23）：旧实现只要历史上出现过 approved 就计入，导致 quarantine 无法撤销已批准
 *  —— 与 evolver-recall.mjs / evolver-bridge.ts 的 2026-09-17 修复对齐（此前遗漏本处）。
 *  修复（0.31）：子串匹配改为 `isApprovedState` 精确比对。 */
export function approvedAssetIds() {
  const latestState = new Map();
  for (const r of readReview()) {
    if (r && typeof r.assetId === 'string' && r.assetId) {
      latestState.set(String(r.assetId).replace(/^"|"$/g, ''), r.state);
    }
  }
  const set = new Set();
  for (const [assetId, state] of latestState) {
    // 0.31 安全修复：改为**精确比对**。旧写法 `includes('approv')` 会把 'unapproved' /
    // 'disapproved' 当成已批准 ⇒ 被明确撤销/拒绝的基因仍会被注入（ClawHub clawscan 点名）。
    if (isApprovedState(state)) set.add(assetId);
  }
  return set;
}

/** 由 gene id 找 asset_id（台账写入用） */
export function assetIdOf(geneId) {
  const g = readGenes().find((x) => x.id === geneId);
  return g?.asset_id ?? null;
}

/** 0.30 B-2：溯源自动归因——读本机 `~/.evomap/source.json`（{model, host}）。
 *  0.32 D-2 精确归因：新增**中间层** `~/.evomap/last_source.json`——由召回钩子把
 *  「本轮**实际**服务的模型」透传进来、经 evolver-recall 落盘。
 *  为什么需要它：source.json 是**静态 per-host 默认值**（= 配置里的 primary），
 *  但宿主有 fallback 链（如 primary=agnes-3.0-flash，fallbacks[0]=deepseek-v4-pro），
 *  某轮若实际由 fallback 服务，静态默认会把它误记成 primary ⇒ 归因错误。
 *  且 deposit / register-hit 是 **agent 自己调**的（不是钩子调的），
 *  钩子子进程的 env 传不到那些后续调用 ⇒ 必须经状态文件中转。
 *  优先级：环境变量 EVOX_SOURCE_MODEL/HOST > last_source.json（≤7 天）> source.json（静态默认）> 空。
 *  ⚠️ 语义边界：last_source.json 是「最近一次观测到的服务模型」，不保证与
 *    本次 deposit 所在轮次完全相同（同会话内通常相同；跨会话/空闲后可能过期，由 7 天窗控制）。 */
const LAST_SOURCE_FILE = path.join(os.homedir(), '.evomap', 'last_source.json');
const LAST_SOURCE_MAX_AGE_MS = 7 * 24 * 3600 * 1000;

/** 0.32 D-2：把「本轮实际服务的模型」落盘（由 evolver-recall 在拿到 EVOX_SOURCE_MODEL 时调用）。
 *  host 取值顺序：EVOX_SOURCE_HOST > source.json 里的 host > os.hostname()
 *  （沿用运维在 source.json 里起的名字，避免与 hostname 不一致导致同宿主被算成两个桶） */
export function recordActualSource(model, host) {
  try {
    const m = String(model || '').slice(0, 80);
    if (!m) return false;
    let h = String(host || '').slice(0, 80);
    if (!h) {
      try {
        const cfg = JSON.parse(fs.readFileSync(path.join(os.homedir(), '.evomap', 'source.json'), 'utf8'));
        h = String(cfg.host || '').slice(0, 80);
      } catch { /* 无静态默认 */ }
    }
    if (!h) h = os.hostname().slice(0, 80);
    fs.mkdirSync(path.join(os.homedir(), '.evomap'), { recursive: true });
    fs.writeFileSync(LAST_SOURCE_FILE, JSON.stringify({
      model: m,
      host: h,
      ts: new Date().toISOString(),
    }));
    return true;
  } catch { return false; }
}

export function sourceInfo() {
  const env = {
    model: (process.env.EVOX_SOURCE_MODEL || '').slice(0, 80),
    host: (process.env.EVOX_SOURCE_HOST || '').slice(0, 80),
  };
  if (env.model && env.host) return withKv(env);
  // 0.32 D-2：最近一次实测服务模型优先于静态默认（带 7 天新鲜窗）
  try {
    const cfg = JSON.parse(fs.readFileSync(LAST_SOURCE_FILE, 'utf8'));
    if (cfg && cfg.model && (Date.now() - new Date(cfg.ts).getTime()) < LAST_SOURCE_MAX_AGE_MS) {
      return withKv({ model: env.model || String(cfg.model).slice(0, 80), host: env.host || String(cfg.host || os.hostname()).slice(0, 80) });
    }
  } catch { /* 无或过期 → 走静态默认 */ }
  try {
    const p = path.join(os.homedir(), '.evomap', 'source.json');
    const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
    return withKv({ model: env.model || String(cfg.model || '').slice(0, 80), host: env.host || String(cfg.host || '').slice(0, 80) });
  } catch { return withKv(env); }
}

/** 0.32 B-5：KV 压缩方案族（kv_compression）。
 *  为什么是「压缩方案」而不是「模型血统」（arXiv:2609.36322 的因果证据）：
 *  论文把 DeepSeek 的 CSA 压缩核**原样移植到 Qwen3-0.6B 骨架从头预训练**，仍然复现相位敏感性
 *  ⇒ 决定「位置相关的检索失败」的是**压缩核**（分块 + 固定步长），不是厂商血统。
 *  同族 = 同样式压缩核（步长/窗口相同）⇒ 失败模式可迁移；异族 = 不可直接移植。
 *  取值：none / csa-s4（W=8,S=4，DeepSeek-V4）/ stride2（DeepSeek-V4.1-Flash）/ unknown。
 *  ⚠️ 这是**启发式映射**：闭源/未公开架构的模型一律 unknown，不猜。 */
const KV_COMPRESSION_MAP = [
  [/deepseek-v4\.1|deepseek-v4-1/i, 'stride2'],
  [/deepseek-v4/i, 'csa-s4'],
];
export function kvCompressionOf(model) {
  const m = String(model || '');
  if (!m) return 'unknown';
  if (/unknown|^$/.test(m)) return 'unknown';
  for (const [re, fam] of KV_COMPRESSION_MAP) if (re.test(m)) return fam;
  return 'unknown';
}

/** 给 sourceInfo 的结果补上 kv_compression（env 可显式覆盖） */
function withKv(si) {
  const explicit = (process.env.EVOX_KV_COMPRESSION || '').slice(0, 40);
  return { ...si, kv_compression: explicit || kvCompressionOf(si.model) };
}
