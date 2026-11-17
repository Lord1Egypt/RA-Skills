/**
 * code/gene_share.mjs — 共享基因库：脱敏闸门 + export / submit / import（0.14.9）
 *
 * 红线：私有内容不可泄漏。任何基因离开本机/入池前必过 redactionGate()，命中即 fail-closed。
 * 底座：与 light-cli 共用同一 light store 模块（asset_id 去重 / review LWW）。
 *
 * 安全设计：import 的审核态由**操作者用 --tier 指定的池信任级别**决定，
 *   绝不读取基因文件里自称的 provenance.tier —— 否则恶意池可伪装 official 骗取自动批准。
 *   默认 --tier community（一律待审）；仅当操作者显式信任某个自建池时才 --tier official（自动通过）。
 */
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import { SCENES, isApprovedState, isQuarantinedState } from './engine/light/store.mjs';
import os from 'node:os';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// 修复 #3：默认按**模块自身位置**解析底座（跨平台），不再硬编码某台机的 Windows 路径；
// EVO_SKILL_CODE 仅作为「模块被单独放到别处」时的覆盖（例：私有节点试点暂存目录）。
const SKILL_CODE = process.env.EVO_SKILL_CODE || __dirname;
const store = await import(pathToFileURL(path.join(SKILL_CODE, 'engine/light/store.mjs')).href);
// 0.16.0 Q3-1：恶意基因注入扫描（与脱敏闸门并列的两道安全门）。
// 注：必须在 SKILL_CODE 之后导入（否则 TDZ ReferenceError——2026-10-08 实测踩到）。
let injectionScan = null;
try {
  ({ injectionScan } = await import(pathToFileURL(path.join(SKILL_CODE, 'injection_scan.mjs')).href));
} catch { injectionScan = null; }

const POOL_DIR = process.env.EVO_POOL_DIR || path.join(os.homedir(), '.evomap', 'pool');

// ── 脱敏闸门规则（红线，fail-closed）──────────────────────────────────────
// ⚠️ 默认只含**通用**私有模式（私有IP/本地路径/密钥），不含任何项目私有词——
// 因为本文件会公开发布，不能把使用者的内部代号/地址写进来。
// 项目私有词（内部服务名/代号/自建地址等）由使用者在**本地、不发布**的
// redline.local.json 里自行补充（见 loadRedlineConfig），两边合起来才是完整闸门。
const SECRET_TOKENS = /\b(skh|gho|ghp|clh|sk|pk)_[A-Za-z0-9]{8,}/;
const SECRET_ENV = /\b[A-Za-z0-9_]+_(API_KEY|TOKEN|SECRET|PASSWORD)\b/;
const RULES = [
  { id: 'ip-loopback', re: /\b127\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, why: '回环地址' },
  { id: 'ip-private-10', re: /\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/, why: '私有网段 10/8' },
  { id: 'ip-private-192', re: /\b192\.168\.\d{1,3}\.\d{1,3}\b/, why: '私有网段 192.168/16' },
  { id: 'ip-private-172', re: /\b172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b/, why: '私有网段 172.16/12' },
  { id: 'ip-linklocal', re: /\b169\.254\.\d{1,3}\.\d{1,3}\b/, why: '链路本地地址' },
  { id: 'host-port', re: /\blocalhost:\d+\b/i, why: '本机端口' },
  { id: 'path-win-users', re: /[A-Za-z]:[\\/]+Users[\\/]+/i, why: 'Windows 用户目录' },
  { id: 'path-win-system', re: /[A-Za-z]:[\\/]+Windows[\\/]+/i, why: 'Windows 系统目录' },
  { id: 'path-posix-home', re: /(^|[\s"'`(])(\/root\/|\/home\/[A-Za-z0-9_.-]+\/|\/Users\/[A-Za-z0-9_.-]+\/)/, why: 'POSIX home/用户目录' },
  { id: 'path-unc', re: /\\\\[A-Za-z0-9_.-]+\\/, why: 'UNC 网络路径' },
  { id: 'secret-token', re: SECRET_TOKENS, why: '疑似令牌字面量' },
  { id: 'secret-env', re: SECRET_ENV, why: '疑似密钥环境变量名' },
];
// 白名单仅对歧义规则(allowExempt)生效；确定性规则一律拦截（fail-closed）。
const ALLOW = /\b(skillhub|clawhub|github|evolver|gep|gepx|pi|npm|node|agnes|deepseek)\b/i;

/** 载入使用者本地私有词表（不发布）：EVO_REDLINE_FILE 或 <store>/redline.local.json，格式 ["词",…] 或 {"terms":[…]} */
function loadRedlineConfig() {
  const cand = process.env.EVO_REDLINE_FILE
    || path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'redline.local.json');
  try {
    const raw = JSON.parse(fs.readFileSync(cand, 'utf8'));
    const terms = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.terms) ? raw.terms : []);
    return terms.filter((t) => typeof t === 'string' && t.length >= 2);
  } catch { return []; }
}
const USER_TERMS = loadRedlineConfig();

/**
 * 0.41 / O01：递归收集**导出对象里的每一个字符串**（此前只枚举 7 类固定字段，实测 4/5
 * 藏私货的样本会漏过：notes / metadata.host / 嵌套 evidence[] / 顶层 raw_log）。
 *  invariants：① 与导出序列化同一对象，不再有"导出有、扫描无"的字段；
 *  ② WeakSet 防循环引用；③ 深度上限 64 防病态结构；④ 数组索引与对象键都进 path 便于定位；
 *  ⑤ 只收集 string（RULES 判定不变），不改动任何守卫标准与 fail-closed 语义。
 */
const MAX_SCAN_DEPTH = 64;
function collectTextFields(gene) {
  const out = [];
  const seen = new WeakSet();
  const walk = (v, p, depth) => {
    if (v == null || depth > MAX_SCAN_DEPTH) return;
    if (typeof v === 'string') { if (v.length) out.push([p, v]); return; }
    if (typeof v !== 'object') return;
    if (seen.has(v)) return;
    seen.add(v);
    if (Array.isArray(v)) {
      v.forEach((x, i) => walk(x, `${p}[${i}]`, depth + 1));
    } else {
      for (const [k, x] of Object.entries(v)) walk(x, p ? `${p}.${k}` : k, depth + 1);
    }
  };
  walk(gene, '', 0);
  return out;
}

/** 脱敏闸门：扫描全部文本字段 → { ok, violations:[{rule,why,field,snippet}] } */
export function redactionGate(gene) {
  const violations = [];
  for (const [field, text] of collectTextFields(gene)) {
    for (const r of RULES) {
      const m = r.re.exec(text);
      if (!m) continue;
      if (r.allowExempt) {
        const ctx = text.slice(Math.max(0, m.index - 4), m.index + m[0].length + 4);
        if (ALLOW.test(ctx)) continue;
      }
      violations.push({ rule: r.id, why: r.why, field, snippet: m[0].slice(0, 40) });
    }
    // 使用者本地私有词（来自 redline.local.json，不发布）——大小写不敏感子串匹配
    const lower = text.toLowerCase();
    for (const term of USER_TERMS) {
      if (lower.includes(term.toLowerCase())) violations.push({ rule: 'user-redline', why: '本地私有词表命中', field, snippet: term.slice(0, 40) });
    }
  }
  return { ok: violations.length === 0, violations };
}

/**
 * 合流闸门：脱敏（防私有内容外泄）+ 注入扫描（防恶意基因）。
 * 两道门方向相反但都要过：出（export/submit）查「别把我的私货带出去 / 别带恶意内容」；
 * 入（import）查「别把别人的恶意基因放进来」。
 */
export function safetyGate(gene) {
  const red = redactionGate(gene);
  // 注入扫描模块不可用 ⇒ **fail-closed**：宁可不共享/不导入，也不放行未经扫描的基因
  if (typeof injectionScan !== 'function') return { ok: false, violations: [{ rule: 'injection-scan-unavailable', why: '注入扫描不可用（fail-closed）', field: '-', snippet: '-', gate: 'injection' }] };
  const inj = injectionScan(gene);
  const violations = [...red.violations.map((v) => ({ ...v, gate: 'redaction' })),
                      ...inj.findings.map((f) => ({ rule: f.rule, why: '疑似提示词注入', field: f.where, snippet: f.snippet, gate: 'injection' }))];
  return { ok: violations.length === 0, violations };
}

const exportable = (genes) => {
  // 池语义（2026-10-10 用户拍板）：**本地库=工作区（待审都在这里）；池=已审核通过的共享集合**。
  // submit 只导出 shareable 且 **LWW 审核态=approved** 的基因；待审/未决定留在本地库（计数报告，
  // 提示先 approve 再推池）。旧版只过滤 shareable → 待审基因可进池、导入侧被 official 自动通过，审核门跨机失效。
  const lww = {};
  try { for (const r of store.readReview()) lww[r.assetId] = r.state; } catch { /* 台账缺失按未决定 */ }
  const stateOf = (g) => {
    // 0.31 安全修复：改为精确比对。这里判定的是**池导出资格**——旧写法 `includes('approv')`
    // 会把 'unapproved' / 'disapproved' 判成 approved ⇒ 未审核或已撤销的基因可进共享池，
    // 审核门在他机上失效（本仓六处审批门中危害最大的一处）。
    if (isApprovedState(lww[g.asset_id])) return 'approved';
    if (isQuarantinedState(lww[g.asset_id])) return 'quarantined';
    return 'undecided';
  };
  const out = [], blocked = [], pending = [], sidecar = [];
  for (const g of genes) {
    if (g?.shareable !== true) continue;
    // 0.42 D13：派生元数据一律不写进基因本体。canonicalV2 的签名域包含除 5 个签名元数据外的
    // 全部字段；旧版在此赋 g.trust / g.trust_note，cmdSubmit 再 spread provenance，
    // 使原本 verified 的基因入池后变成 tampered，他机 gene import 直接 BLOCKED
    // （2026-11-15 实测 61 条 / 修复后又发现池内 24 条历史 tampered）。
    // 现在只生成 detached 侧车行，基因对象原样导出，签名域逐字节稳定、可重复推池、不需私钥。
    const sm = (g.generation_meta || {}).source_model || '';
    const sh = (g.generation_meta || {}).source_host || '';
    sidecar.push({ asset_id: g.asset_id,
                   trust: sm && sh ? 'single-source' : 'unknown-source',
                   trust_note: 'single-source = 仅一个沉积源；升级 cross-source 需 ≥2 个不同 (模型|宿主) 的 register-hit 证据',
                   provenance: { source: 'local', tier: 'official', exported_at: new Date().toISOString() } });
    const st = stateOf(g);
    if (st !== 'approved') { pending.push({ id: g.id, state: st }); continue; }
    const gate = safetyGate(g);
    if (gate.ok) out.push(g); else blocked.push({ gene: g, violations: gate.violations });
  }
  return { out, blocked, pending, sidecar };
};
const readJsonl = (p) => { try { return fs.readFileSync(p, 'utf8').split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean); } catch { return []; } };
const writeJsonl = (f, rows) => { fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, rows.map((r) => JSON.stringify(r)).join('\n') + (rows.length ? '\n' : ''), 'utf8'); };
// 池文件写入持锁（与 store.mjs 同一 O_EXCL 协议，见 store.withLock）
const acquirePoolLock = (dir) => {
  const lp = path.join(dir, '.evox.lock');
  try { fs.mkdirSync(dir, { recursive: true }); } catch {}
  const start = Date.now();
  for (;;) {
    try { const fd = fs.openSync(lp, 'wx'); fs.closeSync(fd); return lp; }
    catch (e) {
      if (e && e.code !== 'EEXIST') return null;
      try { const st = fs.statSync(lp); if (Date.now() - st.mtimeMs > 15000) { fs.unlinkSync(lp); continue; } } catch { continue; }
      if (Date.now() - start > 5000) return null;
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 25);
    }
  }
};
const withPoolLock = (dir, fn) => { const lp = acquirePoolLock(dir); try { return fn(); } finally { if (lp) { try { fs.unlinkSync(lp); } catch {} } } };

import { verifyGene, loadIdentity } from './engine/light/identity.mjs';

const argOf = (a, n) => { const i = a.indexOf(n); return i >= 0 ? a[i + 1] : undefined; };
const positional = (a) => a.filter((x, i) => !x.startsWith('--') && !(i > 0 && a[i - 1].startsWith('--')));

function reportBlocked(blocked) {
  for (const b of blocked) { const v = b.violations[0]; console.log(`  [BLOCKED] ${b.gene.id} — 规则 ${v.rule}(${v.why}) 字段 ${v.field} 命中「${v.snippet}」`); }
}

function cmdExport(args) {
  const genes = store.readGenes();
  const { out, blocked, pending } = exportable(genes);
  const dest = argOf(args, '--out') || path.join(POOL_DIR, 'export.jsonl');
  if (out.length) withPoolLock(path.dirname(dest), () => writeJsonl(dest, out));
  console.log(`[gene-share] 库内基因 ${genes.length}｜可导出(shareable+已审核+过闸) ${out.length}｜被闸门拦截 ${blocked.length}｜待审未导出 ${pending.length}`);
  reportBlocked(blocked);
  if (out.length) console.log(`[gene-share] 已导出 → ${dest}`);
  return blocked.length ? 2 : 0;
}

function cmdSubmit(args) {
  // 0.23 G2：--bundle <file> = 单文件提交包（shareable+已审核+过闸 基因 + keyid 署名头），
  // 发给维护者（gene import 默认隔离）或提 PR；不自动推官方池（治理层在人）。
  const bundle = argOf(args, '--bundle');
  if (bundle) {
    const { out, blocked, pending } = exportable(store.readGenes());
    if (!out.length) { console.log('[gene-share] 无可提交基因（shareable+已审核+过闸 均为空）'); return 1; }
    const identity = loadIdentity();
    const header = { type: 'GeneBundle', generated_at: new Date().toISOString(), keyid: identity.keyId, count: out.length };
    fs.mkdirSync(path.dirname(path.resolve(bundle)), { recursive: true });
    fs.writeFileSync(path.resolve(bundle), JSON.stringify(header) + '\n' + out.map((g) => JSON.stringify(g)).join('\n') + '\n');
    console.log(`[gene-share] 提交包已生成 → ${path.resolve(bundle)}（${out.length} 条基因，keyid=${identity.keyId}）`);
    if (blocked.length) { console.log(`[gene-share] 被闸门拦截 ${blocked.length}（未包含）`); reportBlocked(blocked); }
    console.log('[gene-share] 下一步：把该文件发给维护者（PR / issue 附件 / 文件交换）；维护者 gene import 后默认隔离待审。');
    return blocked.length ? 2 : 0;
  }
  const pool = argOf(args, '--pool') || POOL_DIR;
  const { out, blocked, pending, sidecar } = exportable(store.readGenes());
  const dest = path.join(pool, 'genes.jsonl');
  const sideDest = path.join(pool, 'provenance.jsonl');
  const existing = readJsonl(dest);
  const have = new Set(existing.map((g) => g.asset_id));
  let added = 0;
  for (const g of out) {
    if (have.has(g.asset_id)) continue;
    existing.push(g);            // 0.42 D13：原样写入，不追加任何字段
    have.add(g.asset_id); added++;
  }
  withPoolLock(pool, () => {
    writeJsonl(dest, existing);
    const sideExisting = readJsonl(sideDest);
    const sideHave = new Set(sideExisting.map((x) => x.asset_id));
    for (const row of sidecar) if (!sideHave.has(row.asset_id)) { sideExisting.push(row); sideHave.add(row.asset_id); }
    writeJsonl(sideDest, sideExisting);   // detached 侧车：按 asset_id 索引，append-only
  });
  console.log(`[gene-share] 入池 ${added} 条（池中原有 ${existing.length} 条）→ ${dest}`);
  console.log(`[gene-share] 被闸门拦截 ${blocked.length}（未入池，未出网）`);
  if (pending.length) console.log(`[gene-share] 待审未推池 ${pending.length} 条（池=已审核集合；先 approve 再推）: ${pending.slice(0, 5).map((p) => p.id + '(' + p.state + ')').join(', ')}${pending.length > 5 ? ' …' : ''}`);
  reportBlocked(blocked);
  return blocked.length ? 2 : 0;
}

// 0.23 G1：gene pull —— 从本地文件/git URL 拉取基因池。
// 信任模型：官方镜像（--tier official 显式指定）导入 approved；默认 community（隔离待审）。
// 签名验证始终执行：tampered → BLOCKED（0.21 语义）。
// git 操作带 timeout + 有界重试（0.22.0 评测 stability「复杂网络场景容错待验证」的落实）。
// 0.25 维2：pool profiles——~/.evomap/pools.json 命名池源（官方镜像/团队池/本地交换）
const POOLS_FILE = path.join(os.homedir(), '.evomap', 'pools.json');
function resolvePoolName(name) {
  try {
    const cfg = JSON.parse(fs.readFileSync(POOLS_FILE, 'utf8'));
    const p2 = cfg.pools && cfg.pools[name];
    if (p2 && p2.source) return p2.source;
    if (p2 && typeof p2 === 'string') return p2;
  } catch {}
  return null;
}

function resolvePoolSource(src) {
  // 命名池优先（pools.json 有该名则用其 source）
  const named = resolvePoolName(String(src));
  if (named) { console.log(`[gene-share] 池「${src}」→ ${named}`); src = named; }
  const isUrl = /^https?:\/\/|^git@/.test(src);
  if (isUrl && /\.jsonl($|\?)/.test(src)) {
    // 静态 jsonl 文件 URL（如 zyx.pink 镜像）→ HTTPS 下载（timeout 30s + 1 次重试）
    const cache = path.join(os.homedir(), '.evomap', 'pool-cache');
    fs.mkdirSync(cache, { recursive: true });
    const dest = path.join(cache, crypto.createHash('sha256').update(src).digest('hex').slice(0, 12) + '.jsonl');
    const fetchOnce = async () => {
      const ac = typeof AbortSignal !== 'undefined' ? AbortSignal.timeout(30000) : undefined;
      const res = await fetch(src, { signal: ac });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      fs.writeFileSync(dest, Buffer.from(await res.arrayBuffer()));
    };
    return (async () => {
      let ok = false;
      for (let attempt = 1; attempt <= 2 && !ok; attempt++) {
        try { await fetchOnce(); ok = true; } catch (e) { if (attempt >= 2) { console.error(`[gene-share] 镜像下载失败（已重试）: ${e.message}`); return null; } Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 1000); }
      }
      console.log(`[gene-share] 镜像已下载 → ${dest}`);
      return dest;
    })();
  }
  if (!isUrl) {
    if (!fs.existsSync(src)) { console.error(`[gene-share] 池源不存在: ${src}`); return null; }
    if (fs.statSync(src).isDirectory()) {
      const cand = path.join(src, 'genes.jsonl');
      if (fs.existsSync(cand)) return cand;
      console.error(`[gene-share] 目录中无 genes.jsonl: ${src}`); return null;
    }
    return src;
  }
  // git URL → 缓存目录 clone/pull（有界重试 + 超时）
  const cache = path.join(os.homedir(), '.evomap', 'pool-cache');
  fs.mkdirSync(cache, { recursive: true });
  const dir = path.join(cache, crypto.createHash('sha256').update(src).digest('hex').slice(0, 12));
  const run = (args2) => { const r = spawnSync('git', args2, { timeout: 30000, encoding: 'utf8' }); return r; };
  let ok = false;
  for (let attempt = 1; attempt <= 2 && !ok; attempt++) {
    if (fs.existsSync(path.join(dir, '.git'))) {
      const r = run(['-C', dir, 'pull', '--ff-only']);
      ok = r.status === 0;
    } else {
      const r = run(['clone', '--depth', '1', src, dir]);
      ok = r.status === 0;
    }
    if (!ok && attempt < 2) Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 1000);
  }
  if (!ok) { console.error(`[gene-share] git 拉取失败（已重试，timeout 30s）: ${src}`); return null; }
  const cand = path.join(dir, 'genes.jsonl');
  if (!fs.existsSync(cand)) { console.error(`[gene-share] 拉取成功但无 genes.jsonl: ${dir}`); return null; }
  console.log(`[gene-share] 池已拉取 → ${dir}`);
  return cand;
}

async function cmdPull(args) {
  const src = positional(args)[0] || argOf(args, '--pool');
  // 命名池由 resolvePoolSource 内解析
  if (!src) { console.error('[gene-share] pull 需要池源（本地路径或 git URL），或 --pool <源>'); return 1; }
  const tier = argOf(args, '--tier') || 'community';
  const scene = argOf(args, '--scene');
  if (scene && !SCENES.includes(scene)) {
    console.error(`[gene-share] 未知场景: ${scene}（可用: ${SCENES.join(' | ')}）`); return 1;
  }
  let file = await resolvePoolSource(String(src));
  if (!file) return 1;
  if (scene) {
    // 0.24 场景拉取：只导入该场景基因（category 受控词表过滤）；全量池仍在镜像可再拉
    const filtered = path.join(path.dirname(file), `genes-${scene}.jsonl`);
    const poolRows = readJsonl(file);
    const rows = poolRows.filter((g) => g.category === scene);
    if (!rows.length) { console.error(`[gene-share] 场景 ${scene} 在池中为空（池共 ${poolRows.length} 条；可用: ${SCENES.join('|')}）`); return 1; }
    fs.writeFileSync(filtered, rows.map((g) => JSON.stringify(g)).join('\n') + '\n');
    file = filtered;
    console.log(`[gene-share] 场景过滤: ${rows.length}/${poolRows.length} 条 → ${scene}`);
  }
  console.log(`[gene-share] 以 tier=${tier} 导入（签名验证始终执行）`);
  return cmdImport([file, '--tier', tier]);
}

function cmdImport(args) {
  const file = positional(args)[0] || path.join(POOL_DIR, 'genes.jsonl');
  if (!fs.existsSync(file)) { console.error(`[gene-share] 池文件不存在: ${file}`); return 1; }
  // 审核态由**操作者指定的池信任级别**决定（不读基因自称的 tier）：official=自建策展池→自动通过；community=默认→待审。
  const tier = argOf(args, '--tier') === 'official' ? 'official' : 'community';
  const state = tier === 'official' ? 'approved' : 'quarantined';
  let added = 0, skipped = 0, blocked = 0;
  for (const g of readJsonl(file)) {
    // 纵深防御：入库前两道门都过（脱敏 + 注入扫描）
    if (!safetyGate(g).ok) { blocked++; continue; }
    if (g?.shareable !== true) { skipped++; continue; }
    // 0.21 provenance：入池导入验签——内容被篡改（sig 与内容不匹配）拒绝入库；无签名/无法验证按 legacy 接受
    const v = verifyGene(g);
    if (v.status === 'tampered') { console.log(`  [BLOCKED] ${g.id} — 验签失败：${v.why}（拒绝导入）`); blocked++; continue; }
    if (store.appendGene(g)) {
      const reason = `imported from ${tier} pool` + (v.status === 'verified' ? '（签名有效）' : v.status === 'unsigned' ? '（无签名 legacy）' : `（${v.status}）`);
      store.appendReview({ assetId: g.asset_id, state, reason }); added++;
    }
    else skipped++;
  }
  console.log(`[gene-share] 导入(tier=${tier}→${state})：新增 ${added}｜跳过 ${skipped}｜闸门拦截 ${blocked}`);
  return 0;
}

/** 供 light-cli 调用的入口（返回退出码，不自行 process.exit） */
export function runGene(args) {
  const [sub, ...rest] = args;
  if (sub === 'export') return cmdExport(rest);
  if (sub === 'submit') return cmdSubmit(rest);
  if (sub === 'pull') return cmdPull(rest);
  if (sub === 'import') return cmdImport(rest);
  console.log('用法: gene_share.mjs export|import|submit');
  return 1;
}

if (process.argv[1] && fs.realpathSync(path.resolve(process.argv[1])) === fs.realpathSync(fileURLToPath(import.meta.url))) {
  const __rc = runGene(process.argv.slice(2));
  if (__rc && typeof __rc.then === "function") __rc.then((c) => process.exit(typeof c === "number" ? c : 0));
  else process.exit(typeof __rc === "number" ? __rc : 0);
}
