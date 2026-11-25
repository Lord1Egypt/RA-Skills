import { spawn } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { existsSync, readdirSync } from 'node:fs';
import { homedir, totalmem } from 'node:os';
import { lstat, mkdir, readFile, realpath, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { isInvokedDirectly } from './direct.mjs';
import { engineSpec, hasPaidSpend, loadApiConfig, readLedger } from './api-image.mjs';
import { ATTEMPT_IGNORED } from './attempt-outcomes.mjs';
import {
  RATE_LIMIT_STRIKES, STEAL_FACTOR, applyEngineFailure, attemptDisposition, classifyEngineError, engineSetupReason, failureText,
  keepCounts, medianSeconds, paidBudgetLeft, paidMayTake, shouldSteal,
} from './batch-policy.mjs';
import {
  recordStyleScore, resolveSeriesConfig, resolveStyleMethod, shouldHintSeries, splitJobsDocument, styleMeans, stylePrompt,
  styleRefsForEngine, styleRouteAllows, takeStyleScreen,
} from './series-policy.mjs';
import { RUN_MARKER_FILE, removableWorkPath } from './safety.mjs';
import { STDIO_DISCARD, STDIO_PIPE } from './stdio-modes.mjs';

export const JOB_ID_RE = /^[\p{L}\p{N}][\p{L}\p{N}._-]{0,99}$/u;

export function isValidJobId(id) {
  return typeof id === "string" && JOB_ID_RE.test(id);
}

export function jobFileInsideOut(outDir, file) {
  const rel = path.relative(outDir, file);
  return rel !== "" && !rel.startsWith("..") && !path.isAbsolute(rel);
}

export {
  RATE_LIMIT_STRIKES, STEAL_FACTOR, applyEngineFailure, attemptDisposition, classifyEngineError,
  failureText, keepCounts, medianSeconds, paidBudgetLeft, paidMayTake, shouldSteal,
} from './batch-policy.mjs';

// Create the output directory before any engine starts, and return its real path.
// A symlink, or a path with ".." in it, becomes the directory files are actually written in.
export async function prepareOutputDir(dir) {
  await mkdir(dir, { recursive: true });
  return await realpath(dir);
}

// 抢活：一批图共用一个队列，所有引擎同时开工，每个引擎开几条通道，哪条通道空了就接下一张它做得了的活。
// 队列空了以后抢尾单：正在做的那家已经明显超过自己的通常耗时（中位数的 1.5 倍）才允许再做一份，
// 同时最多一份重复；谁先做完用谁，另一份停掉或丢掉。
// 额度用完、没登录或没装：立刻关掉它的全部通道，手上的活退回队列。
// 普通的 429 / 限流先退避，连续失败达到次数才关掉。单张失败换别家再试；输出已存在的跳过（断点续跑）。
const here = path.dirname(fileURLToPath(import.meta.url));
const ENGINES = {
  gemini: { script: 'gemini-image.mjs', ratios: ['1:1', '2:3', '3:2', '3:4', '4:3', '9:16', '16:9'], ratioFlag: '--aspect', maxRefs: 3 },
  jimeng: { script: 'jimeng-image.mjs', ratios: ['21:9', '16:9', '3:2', '4:3', '1:1', '3:4', '2:3', '9:16'], ratioFlag: '--aspect', maxRefs: 10, video: true, textVideo: true },
  codex: { script: 'codex-image.mjs', ratios: null, ratioFlag: '--aspect', maxRefs: Infinity, extra: ['--json'] },
  grok: { script: 'grok-image.mjs', ratios: ['1:1', '16:9', '9:16', '3:2', '2:3'], ratioFlag: '--ratio', maxRefs: 1, video: true },
  lovart: { script: 'lovart.mjs', ratios: null, ratioFlag: '--aspect', maxRefs: Infinity, extra: ['--json'] },
  muse: { script: 'muse-image.py', ratios: ['1:1', '2:3', '3:2', '3:4', '4:3', '9:16', '16:9'], ratioFlag: '--aspect', maxRefs: Infinity },
};
// Pay-per-image last resort. On only when $HOME/.config/imagegen-swarm/api.json exists.
// 只接订阅引擎都接不了的图（都没额度、都试过、或比例和参考图数都不合适），从不抢尾单，花到本批或本月预算就关掉
const API = loadApiConfig();
if (API) {
  const spec = engineSpec(API);
  ENGINES.api = { script: 'api-image.mjs', ratios: null, acceptsRatio: spec.acceptsRatio, ratioFlag: '--aspect', maxRefs: spec.maxRefs, paid: true, extra: ['--json'] };
}
// 通道数以 8GB 内存为基准（M1 实测同时 12 份单张不变慢、内存还剩约 30%）：Gemini、Codex 6 条，即梦、Grok 4 条，Lovart 2 条；
// 按本机内存等比例增减，每家至少 1 条、最多 1.5 倍，Muse 只有一个专用浏览器固定 1 条；排在前面的先接活
// Off switch: an empty file $HOME/.config/imagegen-swarm/engine-off/<engine> skips that engine.
// IMAGE_GEN_ENGINE_OFF can point at another directory.
// An empty file left in $HOME/.config/image-gen/engine-off still counts, so a renamed install
// does not turn a paused engine back on.
function engineOffNames() {
  const dirs = process.env.IMAGE_GEN_ENGINE_OFF
    ? [process.env.IMAGE_GEN_ENGINE_OFF]
    : [path.join(homedir(), '.config', 'imagegen-swarm', 'engine-off'), path.join(homedir(), '.config', 'image-gen', 'engine-off')];
  const names = new Set();
  for (const dir of dirs) if (existsSync(dir)) for (const name of readdirSync(dir)) names.add(name);
  return [...names];
}
const OFF = engineOffNames();
// 各家单张耗时的起始估计（秒），开跑后按本批实测的中位数更新
const TYPICAL_SECONDS = { gemini: 30, jimeng: 35, codex: 35, grok: 55, lovart: 45, muse: 110, api: 30 };
const BASE_LANES = { gemini: 6, jimeng: 4, codex: 6, grok: 4, lovart: 2, muse: 1 };
// IMAGE_GEN_MEMORY_GB 可指定按多大内存来定通道数（想给别的程序留内存时设小一点）
const MEMORY_GB = Number(process.env.IMAGE_GEN_MEMORY_GB ?? totalmem() / 2 ** 30);
const DEFAULT_LANES = Object.fromEntries(Object.entries(BASE_LANES).map(([engine, n]) =>
  [engine, engine === 'muse' ? 1 : Math.max(1, Math.min(Math.round(n * 1.5), Math.round(n * MEMORY_GB / 8)))]));
// API 线路只发网络请求，不占内存，通道数照配置文件的 lanes（默认 4）
if (API) DEFAULT_LANES.api = API.lanes;
function parse(argv) {
  const o = {
    engines: Object.keys(ENGINES), lanes: { ...DEFAULT_LANES }, tries: 3, series: false,
    style: null, styleFile: null, styleRefs: [], styleThreshold: null, styleRetries: null,
    seriesEngines: null, seriesPrefer: null, styleMethod: null,
  };
  for (let i = 0; i < argv.length; i++) {
    const flag = argv[i];
    if (flag === '--help' || flag === '-h') {
      console.log('batch.mjs --jobs <jobs.json> --out <dir> [--engines gemini,jimeng,codex,grok,lovart,muse,api] [--lanes gemini=2,muse=1] [--tries 3]\n' +
        '[--series] [--style <text> | --style-file <path>] [--style-ref <image>]... [--style-threshold 0.72] [--style-retries 2]\n' +
        '[--series-engines gemini,jimeng] [--series-prefer consistent|off] [--style-method auto|structure|clip|palette-histogram]\n' +
        'api is the pay-per-image last resort. It runs only after the user sets it up (see SETUP.md).\n' +
        'It spends price_per_image on images in this job list that no subscription engine can take, and stops at the budgets in that setup.\n' +
        'jobs.json: [{"id": "cat", "prompt": "...", "ref": ["a.png"], "aspect": "1:1", "video": false, "engine": "gemini"}]（ref、aspect、video、engine 可省）\n' +
        'Series mode also accepts {"series": true, "style": "...", "ref": ["anchor.png"], "jobs": [ ... ]}.');
      process.exit(0);
    }
    if (flag === '--series') { o.series = true; continue; }
    const value = argv[++i];
    if (!value) throw new Error("missing value for " + (flag));
    if (flag === '--jobs') o.jobs = path.resolve(value);
    else if (flag === '--out') o.out = path.resolve(value);
    else if (flag === '--engines') o.engines = value.split(',');
    else if (flag === '--lanes') for (const pair of value.split(',')) { const [k, n] = pair.split('='); o.lanes[k] = Number(n); }
    else if (flag === '--tries') o.tries = Number(value);
    else if (flag === '--style') o.style = value;
    else if (flag === '--style-file') o.styleFile = path.resolve(value);
    else if (flag === '--style-ref') o.styleRefs.push(path.resolve(value));
    else if (flag === '--style-threshold') o.styleThreshold = value;
    else if (flag === '--style-retries') o.styleRetries = value;
    else if (flag === '--series-engines') o.seriesEngines = value.split(',').map(name => name.trim()).filter(Boolean);
    else if (flag === '--series-prefer') o.seriesPrefer = value;
    else if (flag === '--style-method') o.styleMethod = value;
    else throw new Error("invalid argument: " + (flag));
  }
  if (!o.jobs || !o.out) throw new Error('require --jobs and --out');
  for (const e of o.engines) {
    if (e === 'api' && !API) throw new Error('api engine is not configured. The user turns it on during setup (see SETUP.md). This command does not create that config.');
    if (!ENGINES[e]) throw new Error("unknown engine: " + (e));
  }
  o.engines = o.engines.filter(e => !OFF.includes(e));
  return o;
}

// Tests point this at fake engine scripts. A normal run always uses this folder.
function engineScript(name) {
  const root = process.env.IMAGE_GEN_TEST_SCRIPTS === 'yes' && process.env.IMAGE_GEN_SCRIPT_DIR
    ? process.env.IMAGE_GEN_SCRIPT_DIR
    : here;
  return path.join(root, name);
}

function runProcess(bin, args, onChild) {
  return new Promise((resolve, reject) => {
    // 单独成一个进程组，抢尾单输了的一份可以连同它起的子进程一起停掉
    const child = spawn(bin, args, { stdio: [STDIO_DISCARD, STDIO_PIPE, STDIO_PIPE], detached: Boolean(onChild) });
    onChild?.(child);
    let stdout = '', stderr = '';
    child.stdout.on('data', d => { stdout += d; });
    child.stderr.on('data', d => { stderr += d; });
    child.on('error', reject);
    child.on('close', code => resolve({ code, stdout, stderr }));
  });
}

// 清单写了比例的图，交回的宽高比差超过 3% 就不算数（codex、lovart、muse 的比例只写在说明里，偶尔不照做）
const PY = process.env.PYTHON ?? (process.platform === 'win32' ? 'python' : 'python3');
// Returns the imgtool JSON: method, score (0 to 1), raw_score and components.
async function scoreStyle(file, anchors, method) {
  const r = await runProcess(PY, [path.join(here, 'imgtool.py'), 'style', file, ...anchors, '--method', method]);
  if (r.code !== 0) throw new Error("imgtool style failed on " + (file) + ": " + (r.stderr));
  const result = JSON.parse(r.stdout);
  if (!Number.isFinite(Number(result.score))) throw new Error("imgtool style returned no score");
  return { ...result, score: Number(result.score) };
}
// Which optional scoring backends are installed. Local check only; never downloads a model.
async function styleBackends() {
  const r = await runProcess(PY, [path.join(here, 'imgtool.py'), 'backends']);
  if (r.code !== 0) throw new Error("imgtool backends failed: " + (r.stderr));
  return JSON.parse(r.stdout);
}
async function ratioOff(file, aspect) {
  const r = await runProcess(PY, [path.join(here, 'imgtool.py'), 'size', file]);
  if (r.code !== 0) throw new Error("imgtool size failed on " + (file) + ": " + (r.stderr));
  const { width: w, height: h } = JSON.parse(r.stdout);
  const [a, b] = aspect.split(':').map(Number);
  return Math.abs(w / h - a / b) / (a / b) > 0.03 ? (w) + "×" + (h) : null;
}

const log = event => console.log(JSON.stringify({ at: new Date().toISOString(), ...event }));

// 并行的另一家可能也写进了 tried，只能删掉自己这次，不能 pop 掉队尾
function untry(job, engine) {
  const at = job.tried.lastIndexOf(engine);
  if (at >= 0) job.tried.splice(at, 1);
}

async function main() {
  if (!process.env.IMAGE_GEN_RUN_ID) process.env.IMAGE_GEN_RUN_ID = randomBytes(8).toString('hex');
  const runId = process.env.IMAGE_GEN_RUN_ID;
  const ownedNames = new Set();
  const o = parse(process.argv.slice(2));
  const raw = JSON.parse(await readFile(o.jobs, 'utf8'));
  const split = splitJobsDocument(raw);
  if (o.style && o.styleFile) throw new Error('pass --style or --style-file, not both');
  const styleText = o.styleFile ? await readFile(o.styleFile, 'utf8') : o.style;
  const series = resolveSeriesConfig({
    flag: o.series, fileSeries: split.series, root: split.root,
    cli: {
      style: styleText, threshold: o.styleThreshold, maxRetries: o.styleRetries,
      engines: o.seriesEngines, prefer: o.seriesPrefer, refs: o.styleRefs, method: o.styleMethod,
    },
  });
  const seriesOptions = o.style || o.styleFile || o.styleRefs.length || o.seriesEngines || o.styleThreshold || o.styleRetries || o.seriesPrefer || o.styleMethod;
  if (!series.enabled && seriesOptions) throw new Error('series options need --series, or "series" in the jobs file');
  const jobs = split.jobs;
  const base = path.dirname(o.jobs);
  const seriesHint = shouldHintSeries({ flag: o.series, root: split.root, jobs, base });
  const ids = new Set();
  for (const job of jobs) {
    if (!job.prompt) throw new Error("every job needs id and prompt: " + (JSON.stringify(job)));
    if (!isValidJobId(job.id)) {
      throw new Error("job id may only use letters, digits, '.', '_' and '-' (max 100 characters, starting with a letter or digit): " + JSON.stringify(job.id));
    }
    if (ids.has(job.id)) throw new Error("duplicate job id: " + (job.id));
    ids.add(job.id);
    job.ref = (job.ref ?? []).map(r => path.resolve(base, r));
    job.tried = [];
    job.active = [];
    job.styleRedos = 0;
  }
  if (series.enabled) {
    series.stats = {};
    series.visualAnchor = null;
    series.anchorJob = null;
    series.textOnly = new Set();
    series.partial = new Set();
    series.styleRefs = series.styleRefs.map(ref => path.isAbsolute(ref) ? ref : path.resolve(base, ref));
    for (const ref of series.styleRefs) {
      if (!existsSync(ref)) throw new Error("series reference not found: " + (ref));
    }
    if (series.engines) {
      for (const name of series.engines) if (!ENGINES[name]) throw new Error("unknown series engine: " + (name));
      const available = series.engines.filter(name => o.engines.includes(name));
      if (!available.length) throw new Error("series engines are not in this batch: " + (series.engines.join(',')));
      series.engines = available;
    }
    // One method for the whole batch, so engine means compare like with like.
    // The probe also checks Python and Pillow before any engine starts.
    series.methodRequested = series.method;
    const backends = await styleBackends();
    const resolved = resolveStyleMethod(series.method, backends);
    series.method = resolved.method;
    series.methodReason = resolved.reason;
    series.components = backends.methods?.[series.method]?.weights ?? null;
  }
  o.out = await prepareOutputDir(o.out);
  if (seriesHint) {
    console.error(JSON.stringify({
      at: new Date().toISOString(), event: 'series_hint',
      message: '这批任务共用同一组参考图，如果要统一风格，可以加 --series。All jobs share the same reference images; add --series if they should share one style.',
    }));
  }
  for (const job of jobs) job.file = path.join(o.out, (job.id) + "." + (job.video ? 'mp4' : 'png'));
  for (const job of jobs) {
    if (!jobFileInsideOut(o.out, job.file)) throw new Error("job file would be written outside --out: " + JSON.stringify(job.id));
  }
  const start = Date.now();
  const down = new Map();
  const setupReasons = new Map();
  let sawNonSetupFailure = false;
  const rateStrikes = new Map();
  const rateBackoffUntil = new Map();
  const done = [], failed = [];
  const queue = [];
  for (const job of jobs) {
    if (existsSync(job.file) && (await stat(job.file)).size > 0) done.push({ id: job.id, file: job.file, engine: 'existing' });
    else queue.push(job);
  }
  const capable = (engine, job, reconsiderPaid = false) => {
    const e = ENGINES[engine];
    const ratioOk = !job.aspect || (e.acceptsRatio ? e.acceptsRatio(job.aspect) : !e.ratios || e.ratios.includes(job.aspect));
    const reconsider = reconsiderPaid && e.paid;
    const budgetDown = reconsider && String(down.get(engine) ?? '').includes('budget used up');
    return (!down.has(engine) || budgetDown) && (!job.tried.includes(engine) || reconsider) && (!job.engine || job.engine === engine)
      && (!job.video || e.video) && ratioOk
      && job.ref.length <= e.maxRefs && (!job.video || job.ref.length > 0 || e.textVideo);
  };
  // 订阅引擎还在限流退避也算接得了：付费线路等它，不为了快去花钱
  const fitsCore = (engine, job) => capable(engine, job) && (!ENGINES[engine].paid || paidMayTake({
    named: job.engine === engine,
    subscriptionCanTake: o.engines.some(other => !ENGINES[other].paid && capable(other, job)),
  }));
  const engineBusy = engine => jobs.reduce((n, job) => n + job.active.filter(active => active.engine === engine).length, 0);
  const styleAllows = (engine, job) => {
    if (!series.enabled) return true;
    const fitting = [];
    const free = {};
    for (const name of o.engines) {
      if (!fitsCore(name, job)) continue;
      if ((rateBackoffUntil.get(name) ?? 0) > Date.now()) continue;
      fitting.push(name);
      const lanes = o.lanes[name] ?? 0;
      free[name] = lanes > 0 && engineBusy(name) < lanes;
    }
    return styleRouteAllows({
      enabled: true, video: Boolean(job.video), engine, allowedEngines: series.engines,
      prefer: series.prefer, scores: series.stats, fitting, free,
    });
  };
  const fits = (engine, job) => fitsCore(engine, job) && styleAllows(engine, job);
  const monthAtStart = API ? readLedger().usd : 0;
  let paidCommitted = 0;
  const paidBudgetReason = () => paidBudgetLeft({ price: API.price, committed: paidCommitted,
    budgetBatch: API.budgetBatch, monthSpent: monthAtStart, budgetMonth: API.budgetMonth });
  const stoppedByBudget = job => {
    if (!API || !o.engines.includes('api') || !capable('api', job, true)) return null;
    if (series.enabled && series.engines && !series.engines.includes('api')) return null;
    if (o.engines.some(engine => !ENGINES[engine].paid && capable(engine, job)
      && (!series.enabled || !series.engines || series.engines.includes(engine)))) return null;
    const reason = paidBudgetReason();
    return reason ? 'api: stopped by the paid budget: ' + reason : null;
  };
  const requeue = job => {
    const reason = stoppedByBudget(job);
    if (reason) {
      failed.push({ id: job.id, tried: job.tried, reason, stopped_by_budget: true });
      log({ event: 'failed', id: job.id, reason });
    } else queue.push(job);
  };
  // 没有任何还开着、还没试过的引擎能接的活，判定失败
  const settleOrphans = () => {
    for (let i = queue.length - 1; i >= 0; i--) {
      const job = queue[i];
      const budgetReason = stoppedByBudget(job);
      if (budgetReason || !o.engines.some(engine => fits(engine, job)) || job.tried.length >= o.tries) {
        queue.splice(i, 1);
        failed.push({ id: job.id, tried: job.tried, reason: budgetReason ?? job.reason ?? '没有能接这张图的引擎（比例、参考图数、视频或额度）',
          ...(budgetReason ? { stopped_by_budget: true } : {}) });
        log({ event: 'failed', id: job.id, reason: failed.at(-1).reason });
      }
    }
  };
  settleOrphans();

  // 每次尝试（成功、失败、被停掉）都记下来，时间线用
  const attempts = [];
  let running = 0, serial = 0;
  // 一次尝试从开工算到收尾（量比例、清临时文件、把没出成的图退回队列）都算正在跑：
  // 别的通道看到没人在跑、队列也空才收工，收尾没做完就把计数减掉的话，退回来的图会没人接
  async function attempt(engine, n, job) {
    running++;
    // Reserve before starting; only a known uncharged failure releases the slot.
    if (ENGINES[engine].paid) paidCommitted++;
    try {
      await attemptOnce(engine, n, job);
    } finally {
      running--;
    }
  }

  async function attemptOnce(engine, n, job) {
    const e = ENGINES[engine];
    job.tried.push(engine);
    const record = { id: job.id, engine, lane: n, started: new Date().toISOString(), produced: false };
    job.active.push(record);
    attempts.push(record);
    // 先写临时文件，赢了才改成正式文件名
    const temp = path.join(o.out, ".attempt-" + (job.id) + "-" + (engine) + "-" + (serial++) + (path.extname(job.file)));
    const spendId = e.paid ? randomBytes(16).toString('hex') : null;
    const existing = await lstat(temp).catch(error => {
      if (error.code !== 'ENOENT') throw error;
      return null;
    });
    if (existing?.isSymbolicLink()) throw new Error("Refusing batch attempt output symlink: " + path.basename(temp));
    ownedNames.add(path.basename(temp));
    const script = engineScript(e.script);
    // The parent of the temp output exists before Muse (or any other engine) is started.
    await prepareOutputDir(path.dirname(temp));
    // Muse 不能用信号停（它的浏览器库收到中断会卡住），改用取消文件
    record.cancelFile = engine === 'muse' ? (temp) + ".cancel" : null;
    if (record.cancelFile) ownedNames.add(path.basename(record.cancelFile));
    let prompt = job.prompt;
    let refs = job.ref;
    if (series.enabled) {
      prompt = stylePrompt(job.prompt, series.style);
      const plan = styleRefsForEngine({ maxRefs: e.maxRefs, jobRefs: job.ref, styleRefs: series.styleRefs, video: Boolean(job.video) });
      refs = plan.refs;
      if (series.styleRefs.length && plan.textOnly && !series.textOnly.has(engine)) {
        series.textOnly.add(engine);
        log({ event: 'style_text_only', engine, reason: plan.reason });
      } else if (series.styleRefs.length && plan.attached < series.styleRefs.length && !series.partial.has(engine)) {
        series.partial.add(engine);
        log({ event: 'style_refs_partial', engine, attached: plan.attached, reason: plan.reason });
      }
    }
    const args = [script, '--prompt', prompt, '--out', temp, ...(e.extra ?? []), ...(record.cancelFile ? ['--cancel-file', record.cancelFile] : []),
      ...(spendId ? ['--spend-id', spendId] : []),
      ...refs.flatMap(r => ['--ref', r]), ...(job.aspect ? [e.ratioFlag, job.aspect] : []), ...(job.video ? ['--video'] : [])];
    log({ event: job.active.length > 1 ? 'steal' : 'start', id: job.id, engine, lane: n });
    const usesPython = script.endsWith('.py');
    const r = await runProcess(usesPython ? PY : process.execPath, args, child => { record.child = child; }).catch(error => {
      if (!usesPython || error.code !== 'ENOENT') throw error;
      return { code: 1, stdout: '', stderr: 'Python runtime not installed' };
    });
    delete record.child;
    record.finished = record.finished ?? new Date().toISOString();
    job.active.splice(job.active.indexOf(record), 1);
    const line = r.stdout.trim().split('\n').at(-1) ?? '';
    // 被停掉的那份，或别人已经交卷的那份，不再当成失败。它若仍交回了文件，只记入 keep.duplicates。
    let report = { status: 'error', reason: (r.stderr || r.stdout).slice(-500) };
    if (line.startsWith('{')) {
      try { report = JSON.parse(line); } catch { report = { status: 'error', reason: line.slice(-500) }; }
    }
    if (e.paid) {
      const hasImage = existsSync(temp) && (await stat(temp)).size > 0;
      const recorded = hasPaidSpend(spendId);
      const returned = report.charged === true || hasImage || recorded;
      const kind = classifyEngineError(failureText(report));
      const uncharged = report.charged === false || kind === 'down' || kind === 'rate_limit';
      // A confirmed image wins over an error classification. Unknown failures
      // keep only the in-memory reservation; the parent never invents ledger rows.
      record.charged = returned ? true : uncharged ? false : null;
      if (record.charged === false) paidCommitted--;
    }
    const settled = record.outcome === 'cancelled' || Boolean(job.won);
    if (!settled) {
      if (r.code === 0 && report.status === 'ok') record.produced = true;
      if (record.produced && job.aspect && !job.video) {
        const off = await ratioOff(temp, job.aspect);
        if (off) {
          report.status = 'error';
          report.reason = "比例不对：要 " + (job.aspect) + "，交回 " + (off);
        }
      }
    } else if (r.code === 0 && line.startsWith('{')) {
      // 别人已经交卷，或这一份被停掉之后仍写出了文件：记成多生成的一份，不改正式结果。
      try {
        const late = JSON.parse(line);
        if (late.status === 'ok') record.produced = true;
      } catch { /* 没有交回图片报告 */ }
    }
    const disposition = attemptDisposition({ cancelled: record.outcome === 'cancelled', won: Boolean(job.won), code: r.code, status: report.status });
    if (disposition === ATTEMPT_IGNORED) {
      record.outcome = 'cancelled';
      await rm(temp, { force: true });
      return;
    }
    if (disposition === 'win' && series.enabled && !job.video) {
      let screened = null;
      try {
        screened = await takeStyleScreen(series, job, anchors => scoreStyle(temp, anchors, series.method), undefined);
      } catch (error) {
        if (job.won || record.outcome === 'cancelled') {
          if (series.anchorJob === job.id && !series.visualAnchor) series.anchorJob = null;
          record.outcome = 'cancelled';
          await rm(temp, { force: true });
          return;
        }
        report.status = 'error';
        report.reason = "style screen failed: " + (error.message);
        record.produced = false;
      }
      if (screened) {
        if (job.won || record.outcome === 'cancelled') {
          if (series.anchorJob === job.id && !series.visualAnchor) series.anchorJob = null;
          record.outcome = 'cancelled';
          await rm(temp, { force: true });
          return;
        }
        if (screened.action !== 'keep') {
          await rm(temp, { force: true });
          record.outcome = screened.action === 'redo' ? 'style_redo' : 'style_rejected';
          record.style_score = screened.score;
          if (screened.detail?.components) record.style_components = screened.detail.components;
          recordStyleScore(series.stats, engine, screened.score);
          job.styleRedos = screened.redos;
          const reason = "style score " + (screened.score) + " below " + (series.threshold);
          job.reason = reason;
          log({ event: record.outcome, id: job.id, engine, score: screened.score, redos: screened.redos, threshold: series.threshold, method: series.method, components: screened.detail?.components });
          if (screened.action === 'redo') untry(job, engine);
          else job.styleExhausted = true;
          if (!job.won && !job.active.length) {
            if (screened.action === 'redo') {
              requeue(job);
            } else {
              failed.push({ id: job.id, tried: job.tried, reason, style_score: screened.score, style_redos: screened.redos, style_components: screened.detail?.components });
              log({ event: 'failed', id: job.id, reason });
            }
          }
          return;
        }
        if (typeof screened.score === 'number') {
          recordStyleScore(series.stats, engine, screened.score);
          record.style_score = screened.score;
          if (screened.detail?.components) record.style_components = screened.detail.components;
          if (screened.detail?.raw_score != null) record.style_raw_score = screened.detail.raw_score;
        }
        if (screened.claim) record.style_anchor = true;
      }
    }
    if (disposition === 'win' && report.status === 'ok') {
      rateStrikes.set(engine, 0);
      job.won = true;
      try {
        await rm(job.file, { force: true });
        await writeFile(job.file, await readFile(temp));
        if (record.style_anchor) series.visualAnchor = job.file;
        await rm(temp, { force: true });
      } catch (error) {
        if (record.style_anchor && !series.visualAnchor) series.anchorJob = null;
        job.won = false;
        throw error;
      }
      record.outcome = 'done';
      const seconds = Math.round((Date.parse(record.finished) - Date.parse(record.started)) / 1000);
      const saved = { id: job.id, file: job.file, engine, lane: n, seconds, started: record.started, finished: record.finished };
      if (record.style_score != null) saved.style_score = record.style_score;
      if (record.style_raw_score != null) saved.style_raw_score = record.style_raw_score;
      if (record.style_components) saved.style_components = record.style_components;
      if (record.style_anchor) saved.style_anchor = true;
      done.push(saved);
      log({ event: 'done', id: job.id, engine, seconds });
      // 同一张图还在别家做的那份停掉：Muse 写取消文件，它删掉自己的侧聊天再退出；其余引擎连同子进程整组发 SIGINT
      for (const other of job.active) {
        other.outcome = 'cancelled';
        other.finished = new Date().toISOString();
        if (other.cancelFile) await writeFile(other.cancelFile, 'cancel');
        else if (other.child) {
          try { process.kill(-other.child.pid, 'SIGINT'); } catch { /* 那一份已经退出，忽略即可 */ }
        }
        log({ event: 'cancel', id: job.id, engine: other.engine });
      }
      return;
    }
    await rm(temp, { force: true });
    record.outcome = 'failed';
    const detail = failureText(report);
    const setupReason = engineSetupReason(detail);
    if (!setupReason || record.produced) sawNonSetupFailure = true;
    job.reason = (engine) + ": " + (setupReason && /[\r\n]/.test(detail.trim()) ? setupReason : detail.slice(0, 600));
    const next = applyEngineFailure({ strikes: rateStrikes.get(engine) ?? 0 }, detail);
    rateStrikes.set(engine, next.strikes);
    if (next.action === 'down') {
      down.set(engine, job.reason);
      if (setupReason) setupReasons.set(engine, setupReason);
      untry(job, engine);
      log({ event: 'engine_down', engine, reason: job.reason, ...(next.strikes ? { rate_limit_strikes: next.strikes } : {}) });
    } else if (next.action === 'backoff') {
      // 限流不算这张已经试过：退避结束后同一家还能再接，连续三次才停用
      untry(job, engine);
      rateBackoffUntil.set(engine, Date.now() + next.backoffSeconds * 1000);
      log({ event: 'rate_limit', id: job.id, engine, strikes: next.strikes, backoff_seconds: next.backoffSeconds, reason: job.reason });
    } else {
      log({ event: 'retry', id: job.id, engine, reason: job.reason });
    }
    // 别家还在做这张就不退回队列。风格次数用尽后不再退回。
    if (!job.active.length && !job.won) {
      if (job.styleExhausted) {
        failed.push({ id: job.id, tried: job.tried, reason: job.reason, style_score: record.style_score, style_redos: job.styleRedos, style_components: record.style_components });
        log({ event: 'failed', id: job.id, reason: job.reason });
      } else {
        requeue(job);
        settleOrphans();
      }
    }
  }

  // 某家单张耗时：本批已完成的取中位数，还没有就用起始估计
  const typical = engine => medianSeconds(done.filter(d => d.engine === engine).map(d => d.seconds), TYPICAL_SECONDS[engine]);

  async function lane(engine, n) {
    while (!down.has(engine)) {
      const until = rateBackoffUntil.get(engine) ?? 0;
      if (until > Date.now()) {
        await new Promise(resolve => setTimeout(resolve, Math.min(1000, until - Date.now())));
        continue;
      }
      const index = queue.findIndex(job => fits(engine, job));
      if (index >= 0 && ENGINES[engine].paid) {
        const over = paidBudgetReason();
        if (over) {
          // 付费线路原本接得了、被预算挡下的图，失败原因写明预算用完
          for (const job of queue) if (fits(engine, job)) job.reason = (engine) + ": " + (over);
          down.set(engine, over);
          log({ event: 'engine_down', engine, reason: over });
          settleOrphans();
          return;
        }
      }
      if (index >= 0) {
        await attempt(engine, n, queue.splice(index, 1)[0]);
        continue;
      }
      // 付费线路不抢尾单
      if (ENGINES[engine].paid) {
        if (running === 0) return;
        await new Promise(resolve => setTimeout(resolve, 1000));
        continue;
      }
      // 队列空了才考虑抢尾单：持有者超过自己中位数的 1.5 倍才抢，已经有一份重复就不再抢。
      // 挑超出比例最大的那张。谁先做完用谁。
      const now = Date.now();
      const overrun = job => ((now - Date.parse(job.active[0].started)) / 1000) / typical(job.active[0].engine);
      const tail = jobs.filter(job => {
        if (job.won || job.active.length !== 1 || !fits(engine, job)) return false;
        const holder = job.active[0];
        const elapsed = (now - Date.parse(holder.started)) / 1000;
        return shouldSteal({ activeCount: job.active.length, holderTypical: typical(holder.engine), holderElapsed: elapsed });
      }).sort((a, b) => overrun(b) - overrun(a))[0];
      if (tail) {
        await attempt(engine, n, tail);
        continue;
      }
      // 暂时没活可接：别的通道还有活在跑就等着（它失败退回的活可能正好归这里），都跑完了才退出
      if (running === 0) return;
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  log({
    event: 'lanes', memory_gb: Math.round(MEMORY_GB),
    lanes: Object.fromEntries(o.engines.map(engine => [engine, o.lanes[engine] ?? 0])),
    ...(series.enabled ? { series: { method: series.method, method_requested: series.methodRequested, method_reason: series.methodReason ?? undefined, threshold: series.threshold, max_retries: series.maxRetries, prefer: series.prefer, engines: series.engines } } : {}),
  });
  const lanes = o.engines.flatMap(engine => Array.from({ length: o.lanes[engine] ?? 0 }, (_, n) => lane(engine, n + 1)));
  await Promise.all(lanes);
  settleOrphans();
  for (const job of queue.splice(0)) failed.push({ id: job.id, tried: job.tried, reason: job.reason ?? '所有通道都已退出' });
  // 只删本轮创建的临时文件，以及带本轮标记的工作目录。别的轮次留下的目录不动。
  for (const name of readdirSync(o.out)) {
    const target = path.join(o.out, name);
    let info;
    try { info = await stat(target); } catch { continue; }
    let marker = '';
    if (info.isDirectory()) {
      try { marker = (await readFile(path.join(target, RUN_MARKER_FILE), 'utf8')).trim(); } catch { marker = ''; }
    }
    if (removableWorkPath({ name, isFile: info.isFile(), marker, runId, ownedNames })) {
      await rm(target, { recursive: true, force: true });
    }
  }
  const byEngine = Object.fromEntries(o.engines.map(engine => [engine, done.filter(d => d.engine === engine).length]));
  const last = done.filter(d => d.finished).map(d => Date.parse(d.finished));
  const charged = attempts.filter(attempt => attempt.charged);
  const paidImages = charged.length;
  const paid = API ? { images: paidImages, usd: Math.round(paidImages * API.price * 10000) / 10000,
    month_usd: readLedger().usd, budget_per_month: API.budgetMonth,
    uncertain: attempts.filter(attempt => attempt.engine === 'api' && attempt.charged === null).length,
    discarded: charged.filter(attempt => attempt.outcome !== 'done').length,
    stopped_by_budget: failed.filter(job => job.stopped_by_budget).length } : undefined;
  // resumed：清单再跑时磁盘上已有的文件，跳过，不算这一轮生成。
  // elapsed_seconds 仍是生成时间：记到引擎交回文件，不含风格打分。
  // delivery_seconds 是从开跑到这份摘要的墙钟，系列模式里含打分和风格重做。
  const keep = { ...keepCounts(attempts), resumed: done.filter(d => d.engine === 'existing').length };
  const delivery_seconds = Math.round((Date.now() - start) / 1000);
  const seriesReport = series.enabled ? {
    method: series.method, method_requested: series.methodRequested, ...(series.methodReason ? { method_reason: series.methodReason } : {}),
    ...(series.components ? { components: series.components } : {}),
    threshold: series.threshold, max_retries: series.maxRetries, prefer: series.prefer,
    engines: series.engines, text_only_engines: [...series.textOnly], partial_ref_engines: [...series.partial],
    engine_style: styleMeans(series.stats),
  } : undefined;
  const selected = [...new Set(o.engines)];
  const setupNeeded = failed.length > 0 && !done.length && !sawNonSetupFailure
    && !failed.some(job => job.stopped_by_budget)
    && selected.length > 0 && selected.every(engine => setupReasons.has(engine));
  const summary = { status: setupNeeded ? 'setup_needed' : failed.length ? 'partial' : 'ok', done: done.length, failed: failed.length, by_engine: byEngine, paid,
    keep, engines_down: Object.fromEntries(down), elapsed_seconds: Math.round(((last.length ? Math.max(...last) : Date.now()) - start) / 1000),
    delivery_seconds, ...(seriesReport ? { series: seriesReport } : {}), ...(seriesHint ? { series_hint: true } : {}),
    results: { done, failed, attempts } };
  await writeFile(path.join(o.out, 'batch-results.json'), JSON.stringify(summary, null, 2));
  log({ event: 'summary', ...summary, results: undefined });
  if (setupNeeded) {
    console.error(['No selected engine could run:',
      ...selected.map(engine => '  ' + engine + ': ' + setupReasons.get(engine)),
      'See SETUP.md for installation and sign-in instructions.',
    ].join('\n'));
  }
  if (failed.length) process.exitCode = 1;
}

if (isInvokedDirectly(import.meta.url)) main().catch(e => { console.log(JSON.stringify({ status: 'error', reason: e.message })); process.exitCode = 1; });
