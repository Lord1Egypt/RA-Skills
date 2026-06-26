import path from "node:path";
import process from "node:process";
import { homedir } from "node:os";
import { fileURLToPath } from "node:url";
import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import type {
  BatchFile,
  BatchTaskInput,
  CliArgs,
  ExtendConfig,
  Provider,
  ProviderModule,
} from "./types";

// ---------------------------------------------------------------------------
// 常量
// ---------------------------------------------------------------------------

const ALL_PROVIDERS: Provider[] = [
  "google", "openai", "azure", "openrouter",
  "dashscope", "minimax", "replicate", "jimeng", "seedream",
];

const REF_CAPABLE_PROVIDERS: Provider[] = [
  "google", "openai", "azure", "openrouter", "replicate", "seedream", "minimax", "jimeng",
];

const MAX_RETRY = 3;
const DEFAULT_MAX_WORKERS = 10;
const POLL_INTERVAL_MS = 250;

type RateLimit = { concurrency: number; startIntervalMs: number };

const DEFAULT_RATE_LIMITS: Record<Provider, RateLimit> = {
  google:     { concurrency: 3, startIntervalMs: 1100 },
  openai:     { concurrency: 3, startIntervalMs: 1100 },
  azure:      { concurrency: 3, startIntervalMs: 1100 },
  openrouter: { concurrency: 3, startIntervalMs: 1100 },
  dashscope:  { concurrency: 3, startIntervalMs: 1100 },
  minimax:    { concurrency: 3, startIntervalMs: 1100 },
  replicate:  { concurrency: 5, startIntervalMs: 700 },
  jimeng:     { concurrency: 3, startIntervalMs: 1100 },
  seedream:   { concurrency: 3, startIntervalMs: 1100 },
};

// ---------------------------------------------------------------------------
// 参数解析
// ---------------------------------------------------------------------------

function collectMany(argv: string[], idx: number): { items: string[]; next: number } {
  const items: string[] = [];
  let j = idx + 1;
  while (j < argv.length && !argv[j]!.startsWith("-")) {
    items.push(argv[j]!);
    j++;
  }
  return { items, next: j - 1 };
}

export function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    prompt: null, promptFiles: [], imagePath: null,
    provider: null, model: null, aspectRatio: null, size: null,
    quality: null, imageSize: null, referenceImages: [],
    n: 1, batchFile: null, jobs: null, json: false, help: false,
  };
  const positional: string[] = [];

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;
    if (a === "-h" || a === "--help") { args.help = true; continue; }
    if (a === "--json") { args.json = true; continue; }

    if (a === "-p" || a === "--prompt") { args.prompt = argv[++i] ?? null; continue; }
    if (a === "--promptfiles") {
      const { items, next } = collectMany(argv, i);
      if (!items.length) throw new Error("--promptfiles 缺少文件参数");
      args.promptFiles.push(...items); i = next; continue;
    }
    if (a === "--image") { args.imagePath = argv[++i] ?? null; continue; }
    if (a === "--batchfile") { args.batchFile = argv[++i] ?? null; continue; }
    if (a === "--jobs") {
      const v = parseInt(argv[++i] ?? "", 10);
      if (isNaN(v) || v < 1) throw new Error("--jobs 需要正整数");
      args.jobs = v; continue;
    }
    if (a === "--provider") {
      const v = argv[++i] as Provider;
      if (!ALL_PROVIDERS.includes(v)) throw new Error(`无效的 provider: ${v}`);
      args.provider = v; continue;
    }
    if (a === "-m" || a === "--model") { args.model = argv[++i] ?? null; continue; }
    if (a === "--ar") { args.aspectRatio = argv[++i] ?? null; continue; }
    if (a === "--size") { args.size = argv[++i] ?? null; continue; }
    if (a === "--quality") {
      const v = argv[++i];
      if (v !== "normal" && v !== "2k") throw new Error(`无效的 quality: ${v}`);
      args.quality = v; continue;
    }
    if (a === "--imageSize") {
      const v = (argv[++i] ?? "").toUpperCase();
      if (v !== "1K" && v !== "2K" && v !== "4K") throw new Error(`无效的 imageSize: ${v}`);
      args.imageSize = v; continue;
    }
    if (a === "--ref" || a === "--reference") {
      const { items, next } = collectMany(argv, i);
      if (!items.length) throw new Error("--ref 缺少文件参数");
      args.referenceImages.push(...items); i = next; continue;
    }
    if (a === "--n") {
      const v = parseInt(argv[++i] ?? "", 10);
      if (isNaN(v) || v < 1) throw new Error("--n 需要正整数");
      args.n = v; continue;
    }
    if (a.startsWith("-")) throw new Error(`未知选项: ${a}`);
    positional.push(a);
  }

  if (!args.prompt && !args.promptFiles.length && positional.length) {
    args.prompt = positional.join(" ");
  }
  return args;
}

// ---------------------------------------------------------------------------
// .env 文件加载
// ---------------------------------------------------------------------------

async function loadEnvFile(filePath: string): Promise<Record<string, string>> {
  try {
    const text = await readFile(filePath, "utf8");
    const env: Record<string, string> = {};
    for (const raw of text.split("\n")) {
      const line = raw.trim();
      if (!line || line.startsWith("#")) continue;
      const eq = line.indexOf("=");
      if (eq < 0) continue;
      const key = line.slice(0, eq).trim();
      let val = line.slice(eq + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'")))
        val = val.slice(1, -1);
      env[key] = val;
    }
    return env;
  } catch { return {}; }
}

async function loadEnv(): Promise<void> {
  const home = homedir();
  const cwd = process.cwd();
  const sources = [
    path.join(home, ".panda-skills", ".env"),
    path.join(cwd, ".panda-skills", ".env"),
    path.join(home, ".baoyu-skills", ".env"),
    path.join(cwd, ".baoyu-skills", ".env"),
  ];
  for (const src of sources) {
    for (const [k, v] of Object.entries(await loadEnvFile(src))) {
      if (!process.env[k]) process.env[k] = v;
    }
  }
}

// ---------------------------------------------------------------------------
// EXTEND.md 配置
// ---------------------------------------------------------------------------

function extractYamlFrontMatter(content: string): string | null {
  const m = content.match(/^---\s*\n([\s\S]*?)\n---/m);
  return m ? m[1]! : null;
}

function parseSimpleYaml(yaml: string): Partial<ExtendConfig> {
  const cfg: Partial<ExtendConfig> = {};
  let section: string | null = null;
  let subProvider: Provider | null = null;

  for (const raw of yaml.split("\n")) {
    const trimmed = raw.trim();
    const indent = (raw.match(/^\s*/) ?? [""])[0].length;
    if (!trimmed || trimmed.startsWith("#")) continue;
    const colon = trimmed.indexOf(":");
    if (colon < 0 || trimmed.startsWith("-")) continue;
    const key = trimmed.slice(0, colon).trim();
    const rawVal = trimmed.slice(colon + 1).trim();
    const val = rawVal === "null" || rawVal === "" ? null : rawVal.replace(/['"]/g, "");

    if (key === "version") { cfg.version = val ? parseInt(val, 10) : 1; continue; }
    if (key === "default_provider") { cfg.default_provider = val as Provider | null; continue; }
    if (key === "default_quality") { cfg.default_quality = val as "normal" | "2k" | null; continue; }
    if (key === "default_aspect_ratio") { cfg.default_aspect_ratio = val; continue; }
    if (key === "default_image_size") { cfg.default_image_size = val as "1K" | "2K" | "4K" | null; continue; }

    if (key === "default_model") {
      cfg.default_model = Object.fromEntries(ALL_PROVIDERS.map(p => [p, null])) as Record<Provider, string | null>;
      section = "default_model"; subProvider = null; continue;
    }
    if (key === "batch") { cfg.batch = {}; section = "batch"; subProvider = null; continue; }

    if (section === "default_model" && ALL_PROVIDERS.includes(key as Provider)) {
      cfg.default_model![key as Provider] = val; continue;
    }
    if (section === "batch" && key === "max_workers") {
      cfg.batch ??= {}; cfg.batch.max_workers = val ? parseInt(val, 10) : null; continue;
    }
    if (section === "batch" && key === "provider_limits") {
      section = "provider_limits"; cfg.batch ??= {}; cfg.batch.provider_limits ??= {}; continue;
    }
    if (section === "provider_limits" && indent >= 4 && ALL_PROVIDERS.includes(key as Provider)) {
      cfg.batch ??= {}; cfg.batch.provider_limits ??= {};
      cfg.batch.provider_limits[key as Provider] ??= {};
      subProvider = key as Provider; continue;
    }
    if (section === "provider_limits" && subProvider && indent >= 6) {
      const numVal = val ? parseInt(val, 10) : null;
      const limits = cfg.batch!.provider_limits![subProvider]!;
      if (key === "concurrency") limits.concurrency = numVal;
      if (key === "start_interval_ms") limits.start_interval_ms = numVal;
    }
  }
  return cfg;
}

async function fileExists(p: string): Promise<boolean> {
  try { await access(p); return true; } catch { return false; }
}

export async function loadExtendConfig(
  cwd = process.cwd(), home = homedir(),
): Promise<Partial<ExtendConfig>> {
  const candidates = [
    path.join(cwd, ".panda-skills", "panda-imagine", "EXTEND.md"),
    path.join(home, ".panda-skills", "panda-imagine", "EXTEND.md"),
    path.join(cwd, ".baoyu-skills", "baoyu-imagine", "EXTEND.md"),
    path.join(home, ".baoyu-skills", "baoyu-imagine", "EXTEND.md"),
  ];
  for (const p of candidates) {
    if (!(await fileExists(p))) continue;
    try {
      const yaml = extractYamlFrontMatter(await readFile(p, "utf8"));
      if (yaml) return parseSimpleYaml(yaml);
    } catch { /* 继续下一个 */ }
  }
  return {};
}

export function mergeConfig(args: CliArgs, ext: Partial<ExtendConfig>): CliArgs {
  return {
    ...args,
    provider: args.provider ?? ext.default_provider ?? null,
    quality: args.quality ?? ext.default_quality ?? null,
    aspectRatio: args.aspectRatio ?? ext.default_aspect_ratio ?? null,
    imageSize: args.imageSize ?? ext.default_image_size ?? null,
  };
}

// ---------------------------------------------------------------------------
// Provider 检测
// ---------------------------------------------------------------------------

function inferProviderFromModel(model: string | null): Provider | null {
  if (!model) return null;
  if (model.includes("seedream") || model.includes("seededit")) return "seedream";
  if (model === "image-01" || model === "image-01-live") return "minimax";
  return null;
}

function isJimengAvailable(): boolean {
  const has = (key: string) => !!process.env[key];
  if (has("JIMENG_ACCESS_KEY_ID") && has("JIMENG_SECRET_ACCESS_KEY")) return true;
  return existsSync(path.join(homedir(), ".dreamina_cli", "credential.json"));
}

function getAvailableProviders(): Provider[] {
  const has = (key: string) => !!process.env[key];
  const available: Provider[] = [];
  if (has("GOOGLE_API_KEY") || has("GEMINI_API_KEY")) available.push("google");
  if (has("OPENAI_API_KEY")) available.push("openai");
  if (has("AZURE_OPENAI_API_KEY") && has("AZURE_OPENAI_BASE_URL")) available.push("azure");
  if (has("OPENROUTER_API_KEY")) available.push("openrouter");
  if (has("DASHSCOPE_API_KEY")) available.push("dashscope");
  if (has("MINIMAX_API_KEY")) available.push("minimax");
  if (has("REPLICATE_API_TOKEN")) available.push("replicate");
  if (isJimengAvailable()) available.push("jimeng");
  if (has("ARK_API_KEY")) available.push("seedream");
  return available;
}

export function detectProvider(args: CliArgs): Provider {
  if (args.referenceImages.length && args.provider && !REF_CAPABLE_PROVIDERS.includes(args.provider)) {
    throw new Error(`--ref 需要支持参考图的 Provider（${REF_CAPABLE_PROVIDERS.join("/")}），当前: ${args.provider}`);
  }
  if (args.provider) return args.provider;

  const modelProvider = inferProviderFromModel(args.model);
  if (modelProvider) {
    const avail = getAvailableProviders();
    if (!avail.includes(modelProvider))
      throw new Error(`模型 "${args.model}" 属于 ${modelProvider}，但未设置对应 API Key`);
    return modelProvider;
  }

  const available = getAvailableProviders();

  if (args.referenceImages.length) {
    for (const p of REF_CAPABLE_PROVIDERS) {
      if (available.includes(p)) return p;
    }
    throw new Error("使用 --ref 需要设置支持参考图的 Provider 的 API Key");
  }

  if (available.length >= 1) return available[0]!;
  throw new Error(
    "未找到任何 API Key。请设置 DASHSCOPE_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY 等环境变量，\n" +
    "或创建 .panda-skills/.env 文件"
  );
}

// ---------------------------------------------------------------------------
// Provider 模块加载
// ---------------------------------------------------------------------------

async function loadProviderModule(provider: Provider): Promise<ProviderModule> {
  switch (provider) {
    case "google":     return import("./providers/google") as Promise<ProviderModule>;
    case "openai":     return import("./providers/openai") as Promise<ProviderModule>;
    case "azure":      return import("./providers/azure") as Promise<ProviderModule>;
    case "openrouter": return import("./providers/openrouter") as Promise<ProviderModule>;
    case "dashscope":  return import("./providers/dashscope") as Promise<ProviderModule>;
    case "minimax":    return import("./providers/minimax") as Promise<ProviderModule>;
    case "replicate":  return import("./providers/replicate") as Promise<ProviderModule>;
    case "jimeng":     return import("./providers/jimeng") as Promise<ProviderModule>;
    case "seedream":   return import("./providers/seedream") as Promise<ProviderModule>;
  }
}

// ---------------------------------------------------------------------------
// Prompt 读取
// ---------------------------------------------------------------------------

async function loadPrompt(args: CliArgs): Promise<string | null> {
  if (args.prompt) return args.prompt;
  if (args.promptFiles.length) {
    const parts: string[] = [];
    for (const f of args.promptFiles) parts.push(await readFile(f, "utf8"));
    return parts.join("\n\n");
  }
  if (!process.stdin.isTTY) {
    try {
      const chunks: Buffer[] = [];
      for await (const chunk of process.stdin)
        chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
      const text = Buffer.concat(chunks).toString("utf8").trim();
      return text || null;
    } catch { return null; }
  }
  return null;
}

// ---------------------------------------------------------------------------
// 模型解析
// ---------------------------------------------------------------------------

function resolveModel(
  provider: Provider, requested: string | null,
  ext: Partial<ExtendConfig>, mod: ProviderModule,
): string {
  if (requested) return requested;
  const fromConfig = ext.default_model?.[provider];
  if (fromConfig) return fromConfig;
  return mod.getDefaultModel();
}

// ---------------------------------------------------------------------------
// 输出路径
// ---------------------------------------------------------------------------

function normalizeOutputPath(p: string, defaultExt = ".png"): string {
  const full = path.resolve(p);
  return path.extname(full) ? full : `${full}${defaultExt}`;
}

// ---------------------------------------------------------------------------
// 参考图校验
// ---------------------------------------------------------------------------

async function validateRefImages(refs: string[]): Promise<void> {
  for (const r of refs) {
    if (!(await fileExists(path.resolve(r))))
      throw new Error(`参考图未找到: ${path.resolve(r)}`);
  }
}

// ---------------------------------------------------------------------------
// 任务定义
// ---------------------------------------------------------------------------

type PreparedTask = {
  id: string;
  prompt: string;
  args: CliArgs;
  provider: Provider;
  model: string;
  outputPath: string;
  providerModule: ProviderModule;
};

type TaskResult = {
  id: string;
  provider: Provider;
  model: string;
  outputPath: string;
  success: boolean;
  attempts: number;
  error: string | null;
};

// ---------------------------------------------------------------------------
// 错误重试判断
// ---------------------------------------------------------------------------

function isRetryable(err: unknown): boolean {
  const msg = err instanceof Error ? err.message : String(err);
  const noRetry = [
    "not supported", "is required", "Invalid ", "API error (400)",
    "API error (401)", "API error (402)", "API error (403)", "API error (404)",
  ];
  return !noRetry.some(m => msg.includes(m));
}

// ---------------------------------------------------------------------------
// 单任务执行（含重试）
// ---------------------------------------------------------------------------

async function executeTask(task: PreparedTask): Promise<TaskResult> {
  console.error(`使用 ${task.provider} / ${task.model}（任务: ${task.id}）`);

  for (let attempt = 1; attempt <= MAX_RETRY; attempt++) {
    try {
      const data = await task.providerModule.generateImage(task.prompt, task.model, task.args);
      await mkdir(path.dirname(task.outputPath), { recursive: true });
      await writeFile(task.outputPath, data);
      return { id: task.id, provider: task.provider, model: task.model, outputPath: task.outputPath, success: true, attempts: attempt, error: null };
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      if (attempt < MAX_RETRY && isRetryable(err)) {
        console.error(`[${task.id}] 第 ${attempt}/${MAX_RETRY} 次失败，重试中...`);
        continue;
      }
      return { id: task.id, provider: task.provider, model: task.model, outputPath: task.outputPath, success: false, attempts: attempt, error: msg };
    }
  }
  return { id: task.id, provider: task.provider, model: task.model, outputPath: task.outputPath, success: false, attempts: MAX_RETRY, error: "未知失败" };
}

// ---------------------------------------------------------------------------
// 单图模式
// ---------------------------------------------------------------------------

async function prepareSingle(args: CliArgs, ext: Partial<ExtendConfig>): Promise<PreparedTask> {
  if (!args.quality) args.quality = "2k";
  const prompt = await loadPrompt(args);
  if (!prompt) throw new Error("缺少 prompt（使用 --prompt 或 --promptfiles）");
  if (!args.imagePath) throw new Error("缺少 --image 输出路径");
  if (args.referenceImages.length) await validateRefImages(args.referenceImages);

  const provider = detectProvider(args);
  const mod = await loadProviderModule(provider);
  const model = resolveModel(provider, args.model, ext, mod);
  mod.validateArgs?.(model, args);
  const defaultExt = mod.getDefaultOutputExtension?.(model, args) ?? ".png";

  return { id: "single", prompt, args, provider, model, outputPath: normalizeOutputPath(args.imagePath, defaultExt), providerModule: mod };
}

async function runSingle(args: CliArgs, ext: Partial<ExtendConfig>): Promise<void> {
  const task = await prepareSingle(args, ext);
  const result = await executeTask(task);
  if (!result.success) throw new Error(result.error ?? "生成失败");

  if (args.json) {
    console.log(JSON.stringify({ savedImage: result.outputPath, provider: result.provider, model: result.model, attempts: result.attempts }, null, 2));
  } else {
    console.log(result.outputPath);
  }
}

// ---------------------------------------------------------------------------
// 批量模式
// ---------------------------------------------------------------------------

async function loadBatchFile(batchPath: string): Promise<{ tasks: BatchTaskInput[]; jobs: number | null; dir: string }> {
  const resolved = path.resolve(batchPath);
  const raw = JSON.parse((await readFile(resolved, "utf8")).replace(/^\uFEFF/, "")) as BatchFile;
  const dir = path.dirname(resolved);
  if (Array.isArray(raw)) return { tasks: raw, jobs: null, dir };
  if (raw && typeof raw === "object" && Array.isArray(raw.tasks)) {
    const jobs = raw.jobs != null ? (typeof raw.jobs === "number" && raw.jobs > 0 ? raw.jobs : null) : null;
    return { tasks: raw.tasks, jobs, dir };
  }
  throw new Error("批量文件格式错误：需要 tasks 数组");
}

function resolveBatchPath(dir: string, p: string): string {
  return path.isAbsolute(p) ? p : path.resolve(dir, p);
}

function buildTaskArgs(base: CliArgs, task: BatchTaskInput, dir: string): CliArgs {
  return {
    ...base,
    prompt: task.prompt ?? null,
    promptFiles: task.promptFiles?.map(f => resolveBatchPath(dir, f)) ?? [],
    imagePath: task.image ? resolveBatchPath(dir, task.image) : null,
    provider: (task.provider ?? base.provider ?? null) as Provider | null,
    model: task.model ?? base.model ?? null,
    aspectRatio: task.ar ?? base.aspectRatio ?? null,
    size: task.size ?? base.size ?? null,
    quality: task.quality ?? base.quality ?? null,
    imageSize: task.imageSize ?? base.imageSize ?? null,
    referenceImages: task.ref?.map(f => resolveBatchPath(dir, f)) ?? [],
    n: task.n ?? base.n,
    batchFile: null, jobs: base.jobs, json: base.json, help: false,
  };
}

async function prepareBatch(args: CliArgs, ext: Partial<ExtendConfig>): Promise<{ tasks: PreparedTask[]; jobs: number | null }> {
  if (!args.batchFile) throw new Error("缺少 --batchfile");
  const { tasks: inputs, jobs, dir } = await loadBatchFile(args.batchFile);
  if (!inputs.length) throw new Error("批量文件中没有任务");

  const prepared: PreparedTask[] = [];
  for (let i = 0; i < inputs.length; i++) {
    const taskArgs = buildTaskArgs(args, inputs[i]!, dir);
    const prompt = await loadPrompt(taskArgs);
    if (!prompt) throw new Error(`任务 ${i + 1} 缺少 prompt`);
    if (!taskArgs.imagePath) throw new Error(`任务 ${i + 1} 缺少 image 输出路径`);
    if (taskArgs.referenceImages.length) await validateRefImages(taskArgs.referenceImages);

    const provider = detectProvider(taskArgs);
    const mod = await loadProviderModule(provider);
    const model = resolveModel(provider, taskArgs.model, ext, mod);
    mod.validateArgs?.(model, taskArgs);
    const defaultExt = mod.getDefaultOutputExtension?.(model, taskArgs) ?? ".png";

    prepared.push({
      id: inputs[i]!.id || `task-${String(i + 1).padStart(2, "0")}`,
      prompt, args: taskArgs, provider, model,
      outputPath: normalizeOutputPath(taskArgs.imagePath, defaultExt),
      providerModule: mod,
    });
  }
  return { tasks: prepared, jobs: args.jobs ?? jobs };
}

// ---------------------------------------------------------------------------
// 并行调度 + Provider 限流
// ---------------------------------------------------------------------------

function getMaxWorkers(ext: Partial<ExtendConfig>): number {
  const env = process.env.BAOYU_IMAGE_GEN_MAX_WORKERS;
  const envVal = env ? parseInt(env, 10) : NaN;
  return Math.max(1, !isNaN(envVal) ? envVal : (ext.batch?.max_workers ?? DEFAULT_MAX_WORKERS));
}

function getProviderLimits(ext: Partial<ExtendConfig>): Record<Provider, RateLimit> {
  const out = {} as Record<Provider, RateLimit>;
  for (const p of ALL_PROVIDERS) {
    const base = DEFAULT_RATE_LIMITS[p];
    const cfgLimit = ext.batch?.provider_limits?.[p];
    const envPrefix = `BAOYU_IMAGE_GEN_${p.toUpperCase()}`;
    const envConc = process.env[`${envPrefix}_CONCURRENCY`];
    const envInterval = process.env[`${envPrefix}_START_INTERVAL_MS`];
    out[p] = {
      concurrency: (envConc ? parseInt(envConc, 10) : NaN) || cfgLimit?.concurrency || base.concurrency,
      startIntervalMs: (envInterval ? parseInt(envInterval, 10) : NaN) || cfgLimit?.start_interval_ms || base.startIntervalMs,
    };
  }
  return out;
}

function createGate(limits: Record<Provider, RateLimit>) {
  const state = new Map<Provider, { active: number; lastStart: number }>();

  return async function acquire(provider: Provider): Promise<() => void> {
    const limit = limits[provider];
    while (true) {
      const cur = state.get(provider) ?? { active: 0, lastStart: 0 };
      const now = Date.now();
      if (cur.active < limit.concurrency && now - cur.lastStart >= limit.startIntervalMs) {
        state.set(provider, { active: cur.active + 1, lastStart: now });
        return () => {
          const s = state.get(provider)!;
          state.set(provider, { active: Math.max(0, s.active - 1), lastStart: s.lastStart });
        };
      }
      await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    }
  };
}

async function runBatch(args: CliArgs, ext: Partial<ExtendConfig>): Promise<void> {
  const { tasks, jobs } = await prepareBatch(args, ext);

  if (tasks.length === 1) {
    const result = await executeTask(tasks[0]!);
    if (!result.success) { process.exitCode = 1; }
    printBatchSummary([result]);
    if (args.json) emitJson([result]);
    return;
  }

  const maxW = getMaxWorkers(ext);
  const limits = getProviderLimits(ext);
  const gate = createGate(limits);
  const workerCount = Math.max(1, Math.min(jobs ?? Math.min(tasks.length, maxW), tasks.length, maxW));

  console.error(`批量模式: ${tasks.length} 个任务, ${workerCount} 个 worker`);

  let nextIdx = 0;
  const results: TaskResult[] = new Array(tasks.length);

  const worker = async () => {
    while (true) {
      const idx = nextIdx++;
      if (idx >= tasks.length) return;
      const task = tasks[idx]!;
      const release = await gate(task.provider);
      try { results[idx] = await executeTask(task); }
      finally { release(); }
    }
  };

  await Promise.all(Array.from({ length: workerCount }, () => worker()));
  printBatchSummary(results);
  if (args.json) emitJson(results);
  if (results.some(r => !r.success)) process.exitCode = 1;
}

function printBatchSummary(results: TaskResult[]): void {
  const ok = results.filter(r => r.success).length;
  const fail = results.length - ok;
  console.error(`\n批量生成摘要: 总计 ${results.length} | 成功 ${ok} | 失败 ${fail}`);
  for (const r of results.filter(r => !r.success)) {
    console.error(`  ✗ ${r.id}: ${r.error}`);
  }
}

function emitJson(results: TaskResult[]): void {
  console.log(JSON.stringify({
    mode: "batch", total: results.length,
    succeeded: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    results,
  }, null, 2));
}

// ---------------------------------------------------------------------------
// 帮助信息
// ---------------------------------------------------------------------------

function printHelp(): void {
  console.log(`panda-imagine — 多 Provider 图片生成引擎

用法:
  bun scripts/main.ts --prompt "描述" --image out.png
  bun scripts/main.ts --promptfiles prompt.md --image out.png --ar 16:9
  bun scripts/main.ts --batchfile batch.json

选项:
  -p, --prompt <text>       提示词文本
  --promptfiles <files...>  从文件读取提示词（多文件拼接）
  --image <path>            输出图片路径
  --batchfile <path>        批量任务 JSON 文件
  --jobs <count>            批量模式 worker 数量（默认自动）
  --provider <name>         强制指定 Provider
  -m, --model <id>          模型 ID
  --ar <ratio>              宽高比（如 16:9, 3:4）
  --size <WxH>              尺寸（如 1024x1024）
  --quality normal|2k       质量预设（默认 2k）
  --imageSize 1K|2K|4K      图片尺寸（Google/OpenRouter）
  --ref <files...>          参考图（Google, OpenAI, MiniMax, Seedream, 即梦CLI 等）
  --n <count>               生成数量
  --json                    JSON 输出
  -h, --help                显示帮助

Provider:
  google | openai | azure | openrouter | dashscope | minimax | replicate | jimeng | seedream

环境变量:
  OPENAI_API_KEY, GOOGLE_API_KEY, DASHSCOPE_API_KEY, MINIMAX_API_KEY,
  REPLICATE_API_TOKEN, ARK_API_KEY, OPENROUTER_API_KEY,
  JIMENG_ACCESS_KEY_ID + JIMENG_SECRET_ACCESS_KEY（或安装 dreamina CLI）,
  AZURE_OPENAI_API_KEY + AZURE_OPENAI_BASE_URL`);
}

// ---------------------------------------------------------------------------
// 入口
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { printHelp(); return; }

  await loadEnv();
  const ext = await loadExtendConfig();
  const merged = mergeConfig(args, ext);
  if (!merged.quality) merged.quality = "2k";

  if (merged.batchFile) {
    await runBatch(merged, ext);
  } else {
    await runSingle(merged, ext);
  }
}

function isDirectExecution(metaUrl: string): boolean {
  const entry = process.argv[1];
  if (!entry) return false;
  try { return path.resolve(entry) === fileURLToPath(metaUrl); }
  catch { return false; }
}

if (isDirectExecution(import.meta.url)) {
  main().catch(err => {
    console.error(err instanceof Error ? err.message : String(err));
    process.exit(1);
  });
}
