/**
 * v5.7.3 配置诊断模块
 *
 * 启动期 + 工具按需，主动检查 ~/.openclaw/openclaw.json 里常见的"导致 Context limit exceeded"陷阱：
 *
 * 1. 缺失 agents.defaults.compaction.reserveTokensFloor — openclaw 4.22 默认值过小
 * 2. reserveTokensFloor 异常（< 5000 或 > 100000）
 * 3. 任意 model 的 maxTokens 占 contextWindow 一半以上 且 > 32000
 *    （openclaw 把 maxTokens 当作必须留给输出的 reserve，吃掉太多 budget）
 *
 * 红线：
 * - 完全只读 openclaw.json，绝不修改用户配置（红线 #1：不侵入式修改 openclaw）
 * - 不用 child_process（红线 #4）
 * - 修复命令通过 return-cliCmd 模式给出，让用户手工或 cron-cli 执行（红线 #5）
 */
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { Type } from "@sinclair/typebox";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import type { ConfigDoctorConfig, NotificationQueue } from "../types.js";
import { DEFAULT_AGENT_ID } from "../types.js";

/**
 * v5.7.4: 检测某条 pluginApi / peerDep 范围是否是合规的 ranged spec。
 * "2026.4.11" → bare（精确匹配，被 openclaw 4.22 拒绝）
 * ">=2026.4.11" / "^2026.4.11" / "~2026.4.11" / "*" / undefined → OK
 *
 * 见 KB `~/.claude/projects/-Users-jobzhao/memory/openclaw_plugin_compat_rules.md`
 */
function isBarePluginApi(spec: unknown): spec is string {
  if (typeof spec !== "string") return false;
  const s = spec.trim();
  if (!s) return false;
  // 任何带前缀的 range 都 OK
  if (/^(>=|<=|>|<|\^|~|\*|=)/.test(s)) return false;
  // 含空格说明是组合 range（如 ">=1.0 <2.0"）也 OK
  if (/\s/.test(s)) return false;
  // 剩下的就是 bare 字符串（如 "2026.4.11"）
  return /^\d/.test(s);
}

/**
 * v5.7.4 / v5.7.21: 收集所有已装 openclaw 插件的根目录
 * 扫描路径：
 * - {openclawDir}/extensions/<plugin>/
 * - {openclawDir}/node_modules/@scope/<plugin>/
 * - {openclawDir}/node_modules/<plugin>/（无 scope）
 *
 * 复用方：scanInstalledPluginsForBarePluginApi / scanInstalledPluginsForAsyncRegister /
 *         scanInstalledPluginsForLegacyToolFields
 */
function collectInstalledPluginDirs(openclawDir: string): string[] {
  const dirs: string[] = [];

  const extDir = join(openclawDir, "extensions");
  if (existsSync(extDir)) {
    try {
      for (const name of readdirSync(extDir)) {
        const p = join(extDir, name);
        try {
          if (statSync(p).isDirectory()) dirs.push(p);
        } catch {
          /* skip */
        }
      }
    } catch {
      /* 静默 */
    }
  }

  const nmDir = join(openclawDir, "node_modules");
  if (existsSync(nmDir)) {
    try {
      for (const name of readdirSync(nmDir)) {
        if (name === ".bin" || name === ".package-lock.json") continue;
        const p = join(nmDir, name);
        try {
          if (!statSync(p).isDirectory()) continue;
        } catch {
          continue;
        }
        if (name.startsWith("@")) {
          try {
            for (const sub of readdirSync(p)) {
              const sp = join(p, sub);
              try {
                if (statSync(sp).isDirectory()) dirs.push(sp);
              } catch {
                /* skip */
              }
            }
          } catch {
            /* skip */
          }
        } else {
          dirs.push(p);
        }
      }
    } catch {
      /* 静默 */
    }
  }
  return dirs;
}

/**
 * 读 plugin package.json，返回 { pkg, isOpenClawPlugin }；非 openclaw 插件返回 null。
 */
function readPluginPackageJson(dir: string): { pkg: any; pkgPath: string } | null {
  const pkgPath = join(dir, "package.json");
  if (!existsSync(pkgPath)) return null;
  let pkg: any;
  try {
    pkg = JSON.parse(readFileSync(pkgPath, "utf-8"));
  } catch {
    return null;
  }
  if (!pkg?.openclaw?.extensions && !pkg?.peerDependencies?.openclaw) return null;
  return { pkg, pkgPath };
}

/**
 * 解析 plugin 入口源文件路径（pkg.openclaw.extensions[0] / pkg.main / index.ts 兜底）。
 */
function resolvePluginEntryFile(dir: string, pkg: any): string | null {
  const candidates = [
    pkg?.openclaw?.extensions?.[0],
    pkg?.main,
    "index.ts",
    "index.js",
  ].filter((c): c is string => typeof c === "string" && c.length > 0);
  for (const c of candidates) {
    const p = join(dir, c);
    if (existsSync(p)) {
      try {
        if (statSync(p).isFile()) return p;
      } catch {
        /* skip */
      }
    }
  }
  return null;
}

/**
 * v6.6.9: 校验 agents.defaults.model.{primary,fallbacks} 中每个 model 是否在
 * cfg.models.providers[<provider>].models[].id 里有完全匹配（**含大小写**）。
 *
 * 用户实测根因：primary="deepseek/DeepSeek-V4-Pro" 大写驼峰，但 deepseek 后端只认
 * "deepseek-v4-pro" 全小写带连字符 → 第一次 LLM 调用就 400 → "Something went wrong"。
 * 这个 bug **跟 fallback 链中其他 model 是否健康无关** —— 因为命名错的 model 走 model-fallback
 * 链时每个都报相同错（model id 字面量不匹配 provider 端 → 全部 400 chain_exhausted）。
 *
 * 校验方式：
 *   - 把 primary + fallbacks 全部 fullId 收集
 *   - 每个 fullId split 成 provider + bareId
 *   - 在 models.providers[provider].models 找 bareId 完全匹配
 *   - 没找到 → 出错；建议查看其它已注册 model 列出近似 candidate
 */
function checkModelIdRegistration(cfg: Record<string, any>): CheckResult[] {
  const results: CheckResult[] = [];
  const modelSpec = cfg?.agents?.defaults?.model;
  if (!modelSpec) return results;

  const providers: Record<string, { models?: Array<{ id?: string }> }> =
    cfg?.models?.providers ?? {};

  const fullIds: string[] = [];
  if (typeof modelSpec.primary === "string" && modelSpec.primary.trim()) {
    fullIds.push(modelSpec.primary.trim());
  }
  if (Array.isArray(modelSpec.fallbacks)) {
    for (const f of modelSpec.fallbacks) {
      if (typeof f === "string" && f.trim()) fullIds.push(f.trim());
    }
  }

  for (const fullId of fullIds) {
    const slash = fullId.indexOf("/");
    if (slash <= 0) {
      results.push({
        ok: false,
        level: "error",
        category: "model-id-format",
        message: `agents.defaults.model 含非法 id "${fullId}" — 应为 "<provider>/<modelId>" 格式`,
      });
      continue;
    }
    const provider = fullId.slice(0, slash);
    const bareId = fullId.slice(slash + 1);

    const providerSpec = providers[provider];
    if (!providerSpec) {
      results.push({
        ok: false,
        level: "error",
        category: "model-provider-missing",
        message: `agents.defaults.model 中 "${fullId}" 的 provider "${provider}" 在 cfg.models.providers 没注册`,
        fixCommand: `cfg.models.providers 当前注册的 providers: [${Object.keys(providers).join(", ")}]；可能 provider 名拼错`,
      });
      continue;
    }
    const registeredIds: string[] = Array.isArray(providerSpec.models)
      ? providerSpec.models.map((m) => String(m?.id ?? "")).filter(Boolean)
      : [];
    if (registeredIds.includes(bareId)) {
      continue; // 完全匹配 ✓
    }
    // 找近似匹配（大小写不敏感）
    const caseInsensitiveMatch = registeredIds.find(
      (r) => r.toLowerCase() === bareId.toLowerCase(),
    );
    if (caseInsensitiveMatch) {
      results.push({
        ok: false,
        level: "error",
        category: "model-id-case-mismatch",
        message:
          `agents.defaults.model 中 "${fullId}" 的 bare id "${bareId}" 在 ` +
          `cfg.models.providers.${provider}.models 没找到完全匹配（大小写敏感）。` +
          `实际注册的是 "${caseInsensitiveMatch}"——大小写不一致会导致 LLM 调用 400 chain_exhausted ("Something went wrong")`,
        fixCommand:
          `把 agents.defaults.model 里 "${fullId}" 改成 "${provider}/${caseInsensitiveMatch}"，或在 ` +
          `cfg.models.providers.${provider}.models 里把 id 改成 "${bareId}"`,
      });
      continue;
    }
    // 完全找不到
    results.push({
      ok: false,
      level: "error",
      category: "model-id-not-registered",
      message:
        `agents.defaults.model 中 "${fullId}" 的 bare id "${bareId}" 在 ` +
        `cfg.models.providers.${provider}.models 完全不存在（已注册：[${registeredIds.join(", ")}])`,
      fixCommand:
        `检查 model id 拼写；或者在 cfg.models.providers.${provider}.models 添加 ` +
        `{id: "${bareId}", contextWindow: ..., maxTokens: ..., cost: ...}`,
    });
  }

  return results;
}

/**
 * v5.7.4: 扫所有已装插件的 package.json 检测 bare pluginApi
 */
function scanInstalledPluginsForBarePluginApi(openclawDir: string): CheckResult[] {
  const results: CheckResult[] = [];
  for (const dir of collectInstalledPluginDirs(openclawDir)) {
    const meta = readPluginPackageJson(dir);
    if (!meta) continue;
    const name = meta.pkg?.name ?? dir;
    const compatApi = meta.pkg?.openclaw?.compat?.pluginApi;
    if (isBarePluginApi(compatApi)) {
      const fixed = `>=${compatApi}`;
      results.push({
        ok: false,
        level: "warn",
        category: "plugin-bare-pluginApi",
        message: `已装插件 ${name}（${meta.pkgPath}）的 openclaw.compat.pluginApi="${compatApi}" 是 bare 版本，会被解读为精确匹配，与当前 openclaw 不兼容时启动报错"插件要求 ${compatApi}"`,
        fixCommand: `python3 -c "import json,pathlib;p=pathlib.Path('${meta.pkgPath}');c=json.loads(p.read_text());c.setdefault('openclaw',{}).setdefault('compat',{})['pluginApi']='${fixed}';p.write_text(json.dumps(c,indent=2,ensure_ascii=False));print('OK')"`,
      });
    }
  }
  return results;
}

/**
 * v5.7.21: 扫所有已装插件的入口文件检测 `async register(` 反模式。
 * Why: openclaw plugin loader 强制 sync 返回（loader-CLyHx60E.js: "plugin register
 * must be synchronous"），async register 返回 Promise → loader 立刻 guarded.close()
 * → 后续所有 api.registerTool 进 silent no-op，整个插件等于没装。
 * 这是 enhance 自己 5.7.13-5.7.16 踩过的坑（修于 5.7.17）。
 */
function scanInstalledPluginsForAsyncRegister(openclawDir: string): CheckResult[] {
  const results: CheckResult[] = [];
  const ASYNC_REGISTER_RE = /\basync\s+register\s*\(/;
  for (const dir of collectInstalledPluginDirs(openclawDir)) {
    const meta = readPluginPackageJson(dir);
    if (!meta) continue;
    const entry = resolvePluginEntryFile(dir, meta.pkg);
    if (!entry) continue;
    let stat;
    try {
      stat = statSync(entry);
    } catch {
      continue;
    }
    // 防御：> 1MB 跳过（避免扫到 webpack bundle 等）
    if (!stat.isFile() || stat.size > 1024 * 1024) continue;
    let src: string;
    try {
      src = readFileSync(entry, "utf-8");
    } catch {
      continue;
    }
    if (!ASYNC_REGISTER_RE.test(src)) continue;
    const name = meta.pkg?.name ?? dir;
    results.push({
      ok: false,
      level: "error",
      category: "plugin-async-register",
      message:
        `已装插件 ${name}（${entry}）入口里有 \`async register(\`。openclaw loader 强制 sync 返回 ` +
        `（loader-CLyHx60E.js: "plugin register must be synchronous"），async 让 loader ` +
        `立刻 guarded.close()，所有 api.registerTool 进 silent no-op，整个插件等于没装`,
      fixCommand:
        `# 1) 把 async register(api) 改回 register(api)\n` +
        `sed -i.bak 's/async register(/register(/' '${entry}'\n` +
        `# 2) 处理函数体里的 await：把 \`await import("xxx")\` 换成\n` +
        `#    \`createRequire(import.meta.url)("xxx")\`（同步，仍可 try/catch ABI 错误）\n` +
        `# 参考 huo15-openclaw-enhance@5.7.17 commit "fix(register): sync register"`,
    });
  }
  return results;
}

/**
 * v5.7.25: 扫所有已装 channel-plugin 的 manifest 顶层是否缺 `channelConfigs.<channelId>`。
 * Why: openclaw runtime setup 流程要在 plugin 实际加载之前用 `channelConfigs.<id>`
 * 渲染 channel 的 label / description / schema。manifest 只声明 `configSchema.properties.
 * channels.<id>.*` 不够 —— runtime 启动会报：
 *   "channel plugin manifest declares <id> without channelConfigs metadata;
 *    add openclaw.plugin.json#channelConfigs so config schema and setup
 *    surfaces work before runtime loads"
 * 这是 @huo15/wechat-service v0.1-2.2.0 踩过的坑（修于 2.2.1）。
 *
 * 触发条件：manifest 顶层 `channels` 数组非空，且 `channelConfigs` 字段缺失或没覆盖到所有声明的 channelId。
 * 修复命令：参考 wechat-service@2.2.1 的 manifest 结构（channelConfigs.<id> 含 label/description/schema 三段）。
 */
function scanInstalledPluginsForMissingChannelConfigs(openclawDir: string): CheckResult[] {
  const results: CheckResult[] = [];
  for (const dir of collectInstalledPluginDirs(openclawDir)) {
    const manifestPath = join(dir, "openclaw.plugin.json");
    if (!existsSync(manifestPath)) continue;
    let manifest: any;
    try {
      manifest = JSON.parse(readFileSync(manifestPath, "utf-8"));
    } catch {
      continue;
    }
    const declaredChannels: string[] = Array.isArray(manifest?.channels) ? manifest.channels.filter((x: any) => typeof x === "string") : [];
    if (declaredChannels.length === 0) continue;
    const channelConfigs = manifest?.channelConfigs;
    const missing: string[] = [];
    if (!channelConfigs || typeof channelConfigs !== "object") {
      missing.push(...declaredChannels);
    } else {
      for (const cid of declaredChannels) {
        const cfg = channelConfigs[cid];
        if (!cfg || typeof cfg !== "object") missing.push(cid);
      }
    }
    if (missing.length === 0) continue;
    const meta = readPluginPackageJson(dir);
    const name = meta?.pkg?.name ?? dir;
    results.push({
      ok: false,
      level: "warn",
      category: "plugin-missing-channelConfigs",
      message:
        `已装 channel 插件 ${name}（${manifestPath}）声明 channels=[${declaredChannels.join(", ")}] ` +
        `但 manifest 顶层 channelConfigs 缺 [${missing.join(", ")}]。openclaw runtime setup 流程需要 ` +
        `channelConfigs.<id>.{label,description,schema} 在 runtime 加载前可用，否则启动报警告且 setup 向导无法渲染该 channel`,
      fixCommand:
        `# 在 ${manifestPath} 顶层加 channelConfigs 字段（与 configSchema 同级）。范例（参考 @huo15/wechat-service@2.2.1）：\n` +
        `# {\n` +
        `#   "id": "<plugin-id>",\n` +
        `#   "channels": [${declaredChannels.map((c) => `"${c}"`).join(", ")}],\n` +
        `#   "channelConfigs": {\n` +
        missing.map((cid) => `#     "${cid}": { "label": "...", "description": "...", "schema": { "type": "object", "properties": { /* 把 configSchema.properties.channels.${cid} 下的 schema 平移过来 */ } } }`).join(",\n") + "\n" +
        `#   },\n` +
        `#   "configSchema": { ... 保留旧路径作为兼容 ... }\n` +
        `# }`,
    });
  }
  return results;
}

/**
 * v5.7.21: 扫所有已装插件的入口文件检测旧版 tool 字段（schema/handler）。
 * Why: openclaw plugin SDK 现校验 { parameters, execute }（tools-CCfW25J2.js
 * describeMalformedPluginTool: typeof tool.execute !== "function" 直接判 missing），
 * 旧字段 schema/handler 全被 loader 跳过。
 * 这是 huo15-huihuoyun-odoo 1.20.0/1.20.1 踩过的坑（修于 1.20.2）。
 */
function scanInstalledPluginsForLegacyToolFields(openclawDir: string): CheckResult[] {
  const results: CheckResult[] = [];
  const SCHEMA_FIELD_RE = /^\s+schema:\s*\{/m;
  const HANDLER_FIELD_RE = /^\s+(?:async\s+)?handler\s*\(/m;
  // 已用 helper 集中转换字段名的（如 huo15-huihuoyun-odoo@1.20.2 的 toSdkTool）
  // 不算 broken —— 跳过，避免对正确实现误报
  const HELPER_PATTERNS = [
    /\btoSdkTool\b/,
    /\bparameters\s*:\s*schema\b/,
    /\bexecute\s*:\s*handler\b/,
  ];
  for (const dir of collectInstalledPluginDirs(openclawDir)) {
    const meta = readPluginPackageJson(dir);
    if (!meta) continue;
    const entry = resolvePluginEntryFile(dir, meta.pkg);
    if (!entry) continue;
    let stat;
    try {
      stat = statSync(entry);
    } catch {
      continue;
    }
    // 工具大入口允许到 5MB（odoo 是 ~320KB；防御 webpack bundle 才设上限）
    if (!stat.isFile() || stat.size > 5 * 1024 * 1024) continue;
    let src: string;
    try {
      src = readFileSync(entry, "utf-8");
    } catch {
      continue;
    }
    // 必须同时命中 schema: 和 handler( —— 单独的 schema 可能是 Type.Object 之类，handler 也可能是别的事件回调
    if (!SCHEMA_FIELD_RE.test(src) || !HANDLER_FIELD_RE.test(src)) continue;
    // carve-out：已经在 helper 里做了字段转换的（例如 toSdkTool）跳过
    if (HELPER_PATTERNS.some((re) => re.test(src))) continue;
    const schemaCount = (src.match(/^\s+schema:\s*\{/gm) ?? []).length;
    const handlerCount = (src.match(/^\s+(?:async\s+)?handler\s*\(/gm) ?? []).length;
    const name = meta.pkg?.name ?? dir;
    results.push({
      ok: false,
      level: "warn",
      category: "plugin-legacy-tool-fields",
      message:
        `已装插件 ${name}（${entry}）疑似用旧版 tool 字段：schema:{ 出现 ${schemaCount} 处、` +
        `handler( 出现 ${handlerCount} 处。openclaw plugin SDK 现在校验 { parameters, execute }，` +
        `旧字段 schema/handler 被 loader 直接判 malformed 跳过（plugin tool is malformed: missing parameters object / missing execute function）`,
      fixCommand:
        `# 在 register helper 里加字段映射（不必逐个 tool 改）：\n` +
        `# const toSdkTool = (opts: any) => {\n` +
        `#   const { schema, handler, ...rest } = opts;\n` +
        `#   return {\n` +
        `#     ...rest,\n` +
        `#     ...(schema  !== undefined && { parameters: schema  }),\n` +
        `#     ...(handler !== undefined && { execute: handler }),\n` +
        `#   };\n` +
        `# };\n` +
        `# 然后 api.registerTool(toSdkTool(opts))。\n` +
        `# 参考 huo15-huihuoyun-odoo@1.20.2 commit "fix: 修 50+ tool malformed"`,
    });
  }
  return results;
}

interface CheckResult {
  ok: boolean;
  level: "info" | "warn" | "error";
  category: string;
  message: string;
  fixCommand?: string;
}

/**
 * 同步读 openclaw.json 并检查 — 调用方负责 try-catch 隔离启动失败
 */
export function checkOpenClawConfig(
  openclawDir: string,
  options: ConfigDoctorConfig = {},
): CheckResult[] {
  const minFloor = options.minReserveTokensFloor ?? 5000;
  const maxFloor = options.maxReserveTokensFloor ?? 100000;
  const maxModelMax = options.maxModelMaxTokens ?? 32000;

  const path = join(openclawDir, "openclaw.json");
  const results: CheckResult[] = [];

  if (!existsSync(path)) {
    return [
      {
        ok: false,
        level: "warn",
        category: "config-missing",
        message: `未找到 ${path}（openclaw 还没初始化过）`,
        fixCommand: "openclaw configure",
      },
    ];
  }

  let cfg: Record<string, any>;
  try {
    cfg = JSON.parse(readFileSync(path, "utf-8"));
  } catch (err) {
    return [
      {
        ok: false,
        level: "error",
        category: "config-parse-failed",
        message: `openclaw.json 解析失败：${(err as Error).message}`,
        fixCommand: "检查 ~/.openclaw/openclaw.json 的 JSON 语法（多余逗号 / 引号未闭合等）",
      },
    ];
  }

  // 1. agents.defaults.compaction.reserveTokensFloor
  const compaction = cfg?.agents?.defaults?.compaction ?? {};
  const reserveFloor = compaction.reserveTokensFloor;

  if (reserveFloor === undefined || reserveFloor === null) {
    results.push({
      ok: false,
      level: "warn",
      category: "compaction-missing-reserveTokensFloor",
      message:
        "缺少 agents.defaults.compaction.reserveTokensFloor — openclaw 4.22 默认值偏小，长 session 容易 'Context limit exceeded'。推荐 20000",
      fixCommand:
        `python3 -c "import json,pathlib;p=pathlib.Path.home()/'.openclaw'/'openclaw.json';c=json.loads(p.read_text());c.setdefault('agents',{}).setdefault('defaults',{}).setdefault('compaction',{})['reserveTokensFloor']=20000;p.write_text(json.dumps(c,indent=2,ensure_ascii=False));print('OK: reserveTokensFloor=20000')"`,
    });
  } else if (typeof reserveFloor !== "number") {
    results.push({
      ok: false,
      level: "error",
      category: "compaction-invalid-type",
      message: `agents.defaults.compaction.reserveTokensFloor=${JSON.stringify(reserveFloor)} 不是 number`,
      fixCommand: "改 ~/.openclaw/openclaw.json: agents.defaults.compaction.reserveTokensFloor = 20000（数字，不带引号）",
    });
  } else if (reserveFloor < minFloor) {
    results.push({
      ok: false,
      level: "warn",
      category: "compaction-low-reserveTokensFloor",
      message: `agents.defaults.compaction.reserveTokensFloor=${reserveFloor} 偏低（推荐 ≥ 20000，至少 ≥ ${minFloor}）`,
      fixCommand: "改 ~/.openclaw/openclaw.json: agents.defaults.compaction.reserveTokensFloor = 20000",
    });
  } else if (reserveFloor > maxFloor) {
    results.push({
      ok: false,
      level: "error",
      category: "compaction-huge-reserveTokensFloor",
      message: `agents.defaults.compaction.reserveTokensFloor=${reserveFloor} 太大（≥ ${maxFloor}），可能让每次压缩都失败`,
      fixCommand: "改 ~/.openclaw/openclaw.json: agents.defaults.compaction.reserveTokensFloor = 20000",
    });
  }

  // 2. 各 model maxTokens 检查
  const providers = cfg?.models?.providers ?? {};
  if (typeof providers === "object" && providers !== null) {
    for (const [pname, pval] of Object.entries(providers)) {
      const models = (pval as any)?.models ?? [];
      if (!Array.isArray(models)) continue;
      for (const m of models) {
        const ctx = Number(m?.contextWindow ?? 0);
        const maxT = Number(m?.maxTokens ?? 0);
        const id = String(m?.id ?? "?");
        if (!ctx || !maxT) continue;
        // maxTokens 占 contextWindow 一半以上 且 > maxModelMax 阈值
        if (maxT >= ctx / 2 && maxT > maxModelMax) {
          results.push({
            ok: false,
            level: "warn",
            category: "model-maxTokens-too-large",
            message: `${pname}/${id}: maxTokens=${maxT} 占 contextWindow=${ctx} 一半以上（${Math.round((maxT / ctx) * 100)}%），每轮预留输出会吃掉太多 budget。建议 ≤ 16384`,
            fixCommand: `改 ~/.openclaw/openclaw.json: models.providers.${pname}.models[].maxTokens（id=${id}）从 ${maxT} 改为 16384`,
          });
        }
      }
    }
  }

  // v6.6.9: 扫 agents.defaults.model.{primary,fallbacks} 中的 model id 是否在
  // cfg.models.providers[<provider>].models[].id 里有完全匹配（含大小写）
  // 触发：用户实测『新会话第一条"你好"也撞 Something went wrong』根因——
  // primary "deepseek/DeepSeek-V4-Pro" 大写驼峰，但 deepseek 后端只认 "deepseek-v4-pro"
  // 全小写带连字符 → 第一次 LLM 调用就 400 → 整条 fallback 链都因同名 bug 全 400
  results.push(...checkModelIdRegistration(cfg));

  // v5.7.4: 扫所有已装插件的 bare pluginApi（违反 ">=X.Y.Z" 规则的会被 openclaw 拒绝）
  results.push(...scanInstalledPluginsForBarePluginApi(openclawDir));
  // v5.7.21: 扫已装插件的 async register（loader 拒收，整个插件 silent no-op）
  results.push(...scanInstalledPluginsForAsyncRegister(openclawDir));
  // v5.7.21: 扫已装插件的旧版 tool 字段 schema/handler（被 loader 判 malformed 跳过）
  results.push(...scanInstalledPluginsForLegacyToolFields(openclawDir));
  // v5.7.25: 扫已装 channel-plugin 的 manifest 是否缺顶层 channelConfigs.<channelId>（runtime setup 报警）
  results.push(...scanInstalledPluginsForMissingChannelConfigs(openclawDir));

  if (results.length === 0) {
    return [
      {
        ok: true,
        level: "info",
        category: "config-ok",
        message: "openclaw 配置 + 已装插件 pluginApi 全部健康（reserveTokensFloor / model maxTokens / plugin compat 均合规）",
      },
    ];
  }
  return results;
}

function formatResults(results: CheckResult[]): string {
  return results
    .map((r) => {
      const icon = r.ok ? "✅" : r.level === "error" ? "❌" : "⚠️";
      let line = `${icon} [${r.category}] ${r.message}`;
      if (r.fixCommand) line += `\n   → 修复: ${r.fixCommand}`;
      return line;
    })
    .join("\n\n");
}

export function registerConfigDoctor(
  api: OpenClawPluginApi,
  config: ConfigDoctorConfig | undefined,
  notifyQueue: NotificationQueue,
) {
  const openclawDir = resolveOpenClawHome(api);

  // 启动期检查（fire-and-forget，绝不阻塞插件加载）
  try {
    const results = checkOpenClawConfig(openclawDir, config);
    const issues = results.filter((r) => !r.ok);
    if (issues.length > 0) {
      api.logger.warn(`[enhance-config-doctor] 检测到 ${issues.length} 项 openclaw.json 配置问题:`);
      for (const r of issues) {
        api.logger.warn(`  • [${r.level}] ${r.category}: ${r.message}`);
        if (r.fixCommand) api.logger.warn(`    → 修复: ${r.fixCommand}`);
      }
      const hasError = issues.some((r) => r.level === "error");
      notifyQueue.emit(
        DEFAULT_AGENT_ID,
        hasError ? "warn" : "warn",
        "config-doctor",
        `enhance: openclaw.json 检测到 ${issues.length} 项配置问题`,
        formatResults(issues) + "\n\n（运行 enhance_config_doctor 工具看完整诊断）",
      );
    } else {
      api.logger.info("[enhance-config-doctor] openclaw.json 配置健康");
    }
  } catch (err) {
    // 启动检查失败不能让插件 crash —— 静默 + log
    api.logger.error(
      `[enhance-config-doctor] 启动检查失败（不影响插件其它功能）: ${(err as Error).message}`,
    );
  }

  // 工具：手动触发完整诊断（输出可粘贴的 fix 命令）
  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_config_doctor",
      description: "诊断 ~/.openclaw/openclaw.json 是否有 reserveTokensFloor / maxTokens 等导致 'Context limit exceeded' 的陷阱配置；只读，给修复命令不自动改",
      parameters: Type.Object({}),
      async execute() {
        const results = checkOpenClawConfig(openclawDir, config);
        const text = formatResults(results);
        return { content: [{ type: "text" as const, text }] };
      },
    })) as any,
    { name: "enhance_config_doctor" },
  );

  api.logger.info("[enhance] 配置诊断模块已加载（只读，不修改用户配置）");
}
