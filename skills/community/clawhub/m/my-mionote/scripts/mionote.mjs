#!/usr/bin/env node
// Meet妙记 CLI 2.0.1（channel=clawhub）。由 packages/cli 构建生成，请勿手改。
// 源码与许可证（Apache-2.0）：https://github.com/mionote/my-mionote

// packages/cli/src/bin.ts
import { tmpdir as tmpdir2 } from "node:os";

// packages/cli/src/errors.ts
var ExitCode = {
  OK: 0,
  /** 参数或用法错误：修正命令后重试 */
  USAGE: 1,
  /** 未配置 Key 或 Key 失效：引导用户配置，不要重试 */
  AUTH: 2,
  /** 接口、网络或本地 IO 错误 */
  API: 3,
  /** 数据尚未就绪（如转写还没生成）：如实告知用户，稍后再查 */
  NOT_READY: 4
};
var CliError = class extends Error {
  exitCode;
  /** 给 AI 助手的下一步建议，原样输出在错误 JSON 的 hint 字段 */
  hint;
  constructor(exitCode, message, hint) {
    super(message);
    this.name = "CliError";
    this.exitCode = exitCode;
    this.hint = hint;
  }
};
var usageError = (message, hint) => new CliError(ExitCode.USAGE, message, hint);

// packages/cli/src/meta.ts
var VERSION = true ? "2.0.1" : "0.0.0-dev";
var CHANNEL = true ? "clawhub" : "dev";
var MIN_NODE_MAJOR = 18;
function userAgent() {
  return `mionote-cli/${VERSION} (channel=${CHANNEL}; node/${process.versions.node}; ${process.platform})`;
}

// packages/cli/src/args.ts
import { parseArgs } from "node:util";
var GLOBAL_OPTIONS = {
  env: { type: "string" },
  pretty: { type: "boolean" },
  help: { type: "boolean", short: "h" }
};
function parseCommandArgs(argv, spec, command) {
  try {
    const { values, positionals } = parseArgs({
      args: argv,
      options: { ...GLOBAL_OPTIONS, ...spec },
      strict: true,
      allowPositionals: true
    });
    return { values, positionals };
  } catch (e) {
    const err = e;
    const hint = `\u6267\u884C mionote ${command} --help \u67E5\u770B\u53EF\u7528\u53C2\u6570`;
    if (err.code === "ERR_PARSE_ARGS_UNKNOWN_OPTION") {
      const option = /'([^']+)'/.exec(err.message)?.[1] ?? "";
      throw usageError(`\u672A\u77E5\u53C2\u6570 ${option}`.trim(), hint);
    }
    if (err.code === "ERR_PARSE_ARGS_INVALID_OPTION_VALUE") {
      throw usageError(`\u53C2\u6570\u53D6\u503C\u6709\u8BEF: ${err.message}`, `${hint}\uFF1B\u53D6\u503C\u4EE5 - \u5F00\u5934\u65F6\u5199\u6210 --\u53C2\u6570=\u53D6\u503C`);
    }
    throw usageError(err.message, hint);
  }
}
function stringOption(values, key) {
  const value = values[key];
  return typeof value === "string" ? value : void 0;
}
function intOption(values, key, fallback, range) {
  const raw = stringOption(values, key);
  if (raw === void 0) return fallback;
  if (!/^\d+$/.test(raw)) throw usageError(`--${key} \u5FC5\u987B\u662F\u6B63\u6574\u6570\uFF0C\u6536\u5230: ${raw}`);
  const value = Number(raw);
  if (value < range.min || value > range.max) {
    throw usageError(`--${key} \u53D6\u503C\u8303\u56F4 ${range.min}-${range.max}\uFF0C\u6536\u5230: ${value}`);
  }
  return value;
}
function requireMeetingId(positionals, command) {
  if (positionals.length !== 1 || !/^\d+$/.test(positionals[0])) {
    throw usageError(`${command} \u9700\u8981\u4E14\u53EA\u9700\u8981\u4E00\u4E2A\u6570\u5B57\u7EAA\u8981 id`, "\u5148\u7528 mionote meetings list \u67E5\u5230 id");
  }
  return positionals[0];
}
function rejectPositionals(positionals, command) {
  if (positionals.length > 0) {
    throw usageError(`${command} \u4E0D\u63A5\u53D7\u591A\u4F59\u53C2\u6570: ${positionals.join(" ")}`, `\u6267\u884C mionote ${command} --help \u67E5\u770B\u7528\u6CD5`);
  }
}

// packages/cli/src/credentials.ts
import { chmodSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
var FILE_NAME = "credentials.json";
var KEY_PATTERN = /^msk-[A-Za-z0-9_-]{8,}$/;
function configDir(env = process.env, platform = process.platform, home = homedir()) {
  if (env.MIONOTE_CONFIG_DIR) return env.MIONOTE_CONFIG_DIR;
  if (platform === "win32") return join(env.APPDATA || join(home, "AppData", "Roaming"), "mionote");
  return join(env.XDG_CONFIG_HOME || join(home, ".config"), "mionote");
}
function credentialsPath(dir) {
  return join(dir, FILE_NAME);
}
function isValidKeyFormat(key) {
  return KEY_PATTERN.test(key);
}
function maskKey(key) {
  return key.length > 12 ? `msk-****${key.slice(-4)}` : "msk-****";
}
function readStore(dir) {
  let raw;
  try {
    raw = readFileSync(credentialsPath(dir), "utf8");
  } catch (e) {
    if (e.code === "ENOENT") return {};
    throw new CliError(ExitCode.API, `\u8BFB\u53D6\u51ED\u8BC1\u6587\u4EF6\u5931\u8D25: ${e.message}`);
  }
  try {
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    throw new CliError(
      ExitCode.AUTH,
      "\u51ED\u8BC1\u6587\u4EF6\u5DF2\u635F\u574F",
      "\u6267\u884C mionote auth logout \u6E05\u9664\u540E\uFF0C\u518D\u6267\u884C mionote auth set \u91CD\u65B0\u914D\u7F6E"
    );
  }
}
function writeStore(dir, store) {
  mkdirSync(dir, { recursive: true, mode: 448 });
  const target = credentialsPath(dir);
  const temp = `${target}.${process.pid}.tmp`;
  writeFileSync(temp, `${JSON.stringify(store, null, 2)}
`, { mode: 384 });
  chmodSync(temp, 384);
  renameSync(temp, target);
}
function readSavedKey(dir, env) {
  return readStore(dir)[env]?.apiKey;
}
function saveKey(dir, env, key, now = /* @__PURE__ */ new Date()) {
  const store = readStore(dir);
  store[env] = { apiKey: key, savedAt: now.toISOString() };
  writeStore(dir, store);
  return credentialsPath(dir);
}
function removeKey(dir, env) {
  const store = readStore(dir);
  if (!store[env]) return false;
  delete store[env];
  if (Object.keys(store).length === 0) {
    rmSync(credentialsPath(dir), { force: true });
  } else {
    writeStore(dir, store);
  }
  return true;
}
function resolveKey(envVars, dir, env) {
  const fromEnv = envVars.MIONOTE_API_KEY?.trim();
  if (fromEnv) return { key: fromEnv, source: "env" };
  const fromFile = readSavedKey(dir, env);
  if (fromFile) return { key: fromFile, source: "file" };
  return void 0;
}

// packages/cli/src/env.ts
var ENVIRONMENTS = {
  prod: { baseUrl: "https://www.mionote.com.cn/mionote-server-api", label: "\u751F\u4EA7" },
  test: { baseUrl: "https://test.mionote.com.cn/mionote-server-api", label: "\u6D4B\u8BD5" }
};
function resolveEnv(flag, envVar) {
  const value = (flag ?? envVar ?? "prod").trim().toLowerCase();
  if (value === "prod" || value === "test") return value;
  throw usageError(`\u672A\u77E5\u73AF\u5883: ${value}`, "--env \u53EA\u652F\u6301 prod \u6216 test");
}

// packages/cli/src/http.ts
var RETRY_AFTER_CAP_MS = 1e4;
var AUTH_HINT = "Key \u53EF\u80FD\u5DF2\u88AB\u91CD\u7F6E\u6216\u586B\u9519\uFF1A\u8BF7\u7528\u6237\u5728 App\u300C\u6211\u7684 \u2192 \u5999\u8BB0 Skill\u300D\u590D\u5236\u6700\u65B0\u7684 Key\uFF0C\u518D\u6267\u884C mionote auth set";
var defaultSleep = (ms) => new Promise((resolve2) => setTimeout(resolve2, ms));
function backoffMs(attempt, retryAfter) {
  const seconds = retryAfter === null ? Number.NaN : Number(retryAfter);
  if (Number.isFinite(seconds) && seconds >= 0) return Math.min(seconds * 1e3, RETRY_AFTER_CAP_MS);
  return Math.min(1e3 * 2 ** attempt, RETRY_AFTER_CAP_MS);
}
function buildUrl(baseUrl, path, params) {
  const url = new URL(baseUrl.replace(/\/+$/, "") + path);
  for (const [key, value] of Object.entries(params)) {
    if (value !== void 0 && value !== "") url.searchParams.set(key, String(value));
  }
  return url;
}
function toBusinessError(code, message) {
  if (code === 401) return new CliError(ExitCode.AUTH, `\u9274\u6743\u5931\u8D25: ${message}`, AUTH_HINT);
  if (code === 403) return new CliError(ExitCode.API, "\u65E0\u6743\u8BBF\u95EE\u8BE5\u7EAA\u8981", "\u53EA\u80FD\u67E5\u770B\u672C\u4EBA\u521B\u5EFA\u6216\u4ED6\u4EBA\u5206\u4EAB\u7ED9\u672C\u4EBA\u7684\u7EAA\u8981");
  if (code === 410) {
    if (message.includes("\u5C1A\u672A\u751F\u6210")) {
      return new CliError(ExitCode.NOT_READY, message, "\u5982\u5B9E\u544A\u77E5\u7528\u6237\u8BE5\u7EAA\u8981\u7684\u8F6C\u5199\u5C1A\u672A\u5B8C\u6210\uFF0C\u7A0D\u540E\u518D\u67E5");
    }
    return new CliError(ExitCode.API, message, "\u786E\u8BA4\u7EAA\u8981 id \u662F\u5426\u6B63\u786E\uFF0C\u53EF\u5148\u7528 meetings list \u67E5\u627E");
  }
  return new CliError(ExitCode.API, `\u63A5\u53E3\u9519\u8BEF(${code ?? "\u672A\u77E5"}): ${message}`);
}
function createApiClient(options) {
  const fetchImpl = options.fetchImpl ?? fetch;
  const sleep = options.sleep ?? defaultSleep;
  const timeoutMs = options.timeoutMs ?? 3e4;
  const maxRetries = options.maxRetries ?? 2;
  async function get(path, params = {}) {
    const url = buildUrl(options.baseUrl, path, params);
    for (let attempt = 0; ; attempt++) {
      const canRetry = attempt < maxRetries;
      let response;
      try {
        response = await fetchImpl(url, {
          headers: {
            Authorization: `Bearer ${options.apiKey}`,
            "User-Agent": options.userAgent,
            Accept: "application/json"
          },
          signal: AbortSignal.timeout(timeoutMs)
        });
      } catch (e) {
        if (canRetry) {
          await sleep(backoffMs(attempt, null));
          continue;
        }
        const reason = e.name === "TimeoutError" ? `\u8D85\u65F6\uFF08${timeoutMs}ms\uFF09` : e.message;
        throw new CliError(ExitCode.API, `\u7F51\u7EDC\u8BF7\u6C42\u5931\u8D25: ${reason}`, "\u68C0\u67E5\u7F51\u7EDC\u6216\u4EE3\u7406\u540E\u91CD\u8BD5\uFF1B\u53EF\u5148\u6267\u884C mionote doctor");
      }
      if (response.status === 429 || response.status >= 500) {
        if (canRetry) {
          await sleep(backoffMs(attempt, response.headers.get("retry-after")));
          continue;
        }
        if (response.status === 429) {
          throw new CliError(ExitCode.API, "\u89E6\u53D1\u9650\u6D41\uFF08\u6BCF\u4E2A Key \u6BCF\u5206\u949F 120 \u6B21\uFF09", "\u7B49\u5F85\u4E00\u5206\u949F\u540E\u518D\u7EE7\u7EED\uFF0C\u6279\u91CF\u67E5\u8BE2\u8BF7\u4E32\u884C\u8FDB\u884C");
        }
        throw new CliError(ExitCode.API, `\u670D\u52A1\u6682\u65F6\u4E0D\u53EF\u7528\uFF08HTTP ${response.status}\uFF09`, "\u7A0D\u540E\u91CD\u8BD5");
      }
      let body;
      try {
        body = await response.json();
      } catch {
        body = void 0;
      }
      const message = body?.message || body?.desc || `HTTP ${response.status}`;
      if (response.status === 401) throw toBusinessError(401, message);
      if (!body) throw new CliError(ExitCode.API, `\u63A5\u53E3\u8FD4\u56DE\u975E JSON\uFF08HTTP ${response.status}\uFF09`);
      if (!response.ok) throw new CliError(ExitCode.API, `\u8BF7\u6C42\u5931\u8D25\uFF08HTTP ${response.status}\uFF09: ${message}`);
      if (body.code !== 200) throw toBusinessError(body.code, message);
      return body.data;
    }
  }
  return { get };
}

// packages/cli/src/context.ts
var NO_KEY_HINT = "\u8BF7\u7528\u6237\u5728 App\u300C\u6211\u7684 \u2192 \u5999\u8BB0 Skill\u300D\u751F\u6210\u5E76\u590D\u5236 API Key\uFF0C\u7136\u540E\u5728\u7EC8\u7AEF\u6267\u884C mionote auth set \u7C98\u8D34\u4FDD\u5B58\uFF1B\u4E5F\u53EF\u4EE5\u901A\u8FC7 AI \u52A9\u624B\u81EA\u5E26\u7684\u5BC6\u94A5\u914D\u7F6E\u63D0\u4F9B\u73AF\u5883\u53D8\u91CF MIONOTE_API_KEY";
function createContext(values, deps2) {
  const env = resolveEnv(stringOption(values, "env"), deps2.envVars.MIONOTE_ENV);
  const dir = configDir(deps2.envVars);
  return {
    deps: deps2,
    env,
    baseUrl: ENVIRONMENTS[env].baseUrl,
    pretty: values.pretty === true,
    configDir: dir,
    requireKey() {
      const resolved = resolveKey(deps2.envVars, dir, env);
      if (!resolved) throw new CliError(ExitCode.AUTH, `\u672A\u914D\u7F6E API Key\uFF08${env} \u73AF\u5883\uFF09`, NO_KEY_HINT);
      if (!isValidKeyFormat(resolved.key)) {
        const where = resolved.source === "env" ? "\u73AF\u5883\u53D8\u91CF MIONOTE_API_KEY" : "\u672C\u673A\u51ED\u8BC1\u6587\u4EF6";
        throw new CliError(ExitCode.AUTH, `${where}\u91CC\u7684 Key \u683C\u5F0F\u4E0D\u6B63\u786E\uFF08\u5E94\u4EE5 msk- \u5F00\u5934\uFF09`, NO_KEY_HINT);
      }
      return resolved;
    },
    client(key) {
      return createApiClient({
        baseUrl: ENVIRONMENTS[env].baseUrl,
        apiKey: key.key,
        userAgent: userAgent(),
        fetchImpl: deps2.fetchImpl,
        sleep: deps2.sleep
      });
    }
  };
}

// packages/cli/src/commands/types.ts
var ok = (data) => ({ data, exitCode: ExitCode.OK });

// packages/cli/src/commands/auth.ts
async function verifyKey(ctx, key) {
  const groups2 = await ctx.client(key).get("/api/open/v1/groups");
  return groups2?.length ?? 0;
}
var authSet = {
  path: "auth set",
  summary: "\u4FDD\u5B58 API Key \u5230\u672C\u673A\u51ED\u8BC1\u6587\u4EF6\uFF08\u4ECE\u6807\u51C6\u8F93\u5165\u8BFB\u53D6\uFF09",
  help: `\u7528\u6CD5: mionote auth set [--env prod|test]

\u4ECE\u6807\u51C6\u8F93\u5165\u8BFB\u53D6 Key\uFF0C\u9A8C\u8BC1\u6709\u6548\u540E\u4FDD\u5B58\u5230\u672C\u673A\u51ED\u8BC1\u6587\u4EF6\uFF08\u6743\u9650 0600\uFF09\uFF0C\u4E4B\u540E\u7684\u547D\u4EE4\u81EA\u52A8\u4F7F\u7528\u3002
  \u7EC8\u7AEF\u91CC\u76F4\u63A5\u6267\u884C\uFF1A\u63D0\u793A\u540E\u7C98\u8D34 Key\uFF0C\u8F93\u5165\u4E0D\u56DE\u663E
  \u7BA1\u9053\u65B9\u5F0F\uFF1A      printf '%s' "$KEY" | mionote auth set
\u4E0D\u63A5\u53D7\u628A Key \u5199\u5728\u547D\u4EE4\u53C2\u6570\u91CC\uFF08\u4F1A\u7559\u5728\u8FDB\u7A0B\u5217\u8868\u4E0E shell \u5386\u53F2\u4E2D\uFF09\u3002`,
  options: {},
  async run(ctx, { positionals }) {
    if (positionals.length > 0) {
      throw usageError("\u4E0D\u8981\u628A Key \u5199\u5728\u547D\u4EE4\u53C2\u6570\u91CC", `\u6539\u7528\u7BA1\u9053\u4F20\u5165\uFF1Aprintf '%s' "$KEY" | mionote auth set`);
    }
    const key = (await ctx.deps.readSecret("\u8BF7\u7C98\u8D34\u5999\u8BB0 API Key\uFF08msk- \u5F00\u5934\uFF0C\u8F93\u5165\u4E0D\u663E\u793A\uFF09: ")).trim();
    if (!key) throw usageError("\u6CA1\u6709\u8BFB\u5230 Key", NO_KEY_HINT);
    if (!isValidKeyFormat(key)) throw usageError("Key \u683C\u5F0F\u4E0D\u6B63\u786E\uFF0C\u5E94\u4EE5 msk- \u5F00\u5934", NO_KEY_HINT);
    let verified = true;
    let groupCount;
    try {
      groupCount = await verifyKey(ctx, { key, source: "file" });
    } catch (e) {
      if (e instanceof CliError && e.exitCode === ExitCode.AUTH) throw e;
      verified = false;
    }
    const path = saveKey(ctx.configDir, ctx.env, key, ctx.deps.now());
    const warnings = [];
    if (!verified) warnings.push("\u7F51\u7EDC\u539F\u56E0\u672A\u80FD\u9A8C\u8BC1 Key\uFF0C\u5DF2\u5148\u4FDD\u5B58\uFF1B\u53EF\u6267\u884C mionote doctor \u590D\u67E5");
    if (ctx.deps.envVars.MIONOTE_API_KEY) {
      warnings.push("\u5F53\u524D\u8FD8\u8BBE\u7F6E\u4E86\u73AF\u5883\u53D8\u91CF MIONOTE_API_KEY\uFF0C\u5B83\u7684\u4F18\u5148\u7EA7\u9AD8\u4E8E\u51ED\u8BC1\u6587\u4EF6");
    }
    return ok({
      saved: true,
      env: ctx.env,
      key: maskKey(key),
      path,
      verified,
      ...groupCount !== void 0 && { groupCount },
      ...warnings.length > 0 && { warnings }
    });
  }
};
var authStatus = {
  path: "auth status",
  summary: "\u67E5\u770B\u5F53\u524D\u4F7F\u7528\u7684 Key\uFF08\u63A9\u7801\uFF09\u53CA\u662F\u5426\u6709\u6548",
  help: `\u7528\u6CD5: mionote auth status [--env prod|test]

\u8F93\u51FA Key \u63A9\u7801\u3001\u6765\u6E90\uFF08env \u73AF\u5883\u53D8\u91CF / file \u51ED\u8BC1\u6587\u4EF6\uFF09\u5E76\u8054\u7F51\u9A8C\u8BC1\u662F\u5426\u6709\u6548\u3002\u672A\u914D\u7F6E\u6216\u65E0\u6548\u65F6\u9000\u51FA\u7801 2\u3002`,
  options: {},
  async run(ctx, { positionals }) {
    rejectPositionals(positionals, "auth status");
    const key = ctx.requireKey();
    const groupCount = await verifyKey(ctx, key);
    return ok({ env: ctx.env, key: maskKey(key.key), source: key.source, valid: true, groupCount });
  }
};
var authLogout = {
  path: "auth logout",
  summary: "\u5220\u9664\u672C\u673A\u4FDD\u5B58\u7684 Key",
  help: `\u7528\u6CD5: mionote auth logout [--env prod|test]

\u5220\u9664\u5F53\u524D\u73AF\u5883\u4FDD\u5B58\u5728\u672C\u673A\u51ED\u8BC1\u6587\u4EF6\u91CC\u7684 Key\u3002\u4E0D\u5F71\u54CD\u73AF\u5883\u53D8\u91CF MIONOTE_API_KEY\uFF0C\u4E5F\u4E0D\u4F1A\u8BA9 Key \u5728\u670D\u52A1\u7AEF\u5931\u6548
\uFF08\u9700\u8981\u4F5C\u5E9F\u8BF7\u5728 App\u300C\u5999\u8BB0 Skill\u300D\u9875\u9762\u91CD\u7F6E\uFF09\u3002`,
  options: {},
  async run(ctx, { positionals }) {
    rejectPositionals(positionals, "auth logout");
    const removed = removeKey(ctx.configDir, ctx.env);
    return ok({
      env: ctx.env,
      removed,
      ...ctx.deps.envVars.MIONOTE_API_KEY && {
        warning: "\u73AF\u5883\u53D8\u91CF MIONOTE_API_KEY \u4ECD\u7136\u5B58\u5728\uFF0C\u547D\u4EE4\u4F1A\u7EE7\u7EED\u4F7F\u7528\u5B83"
      }
    });
  }
};

// packages/cli/src/commands/doctor.ts
var doctor = {
  path: "doctor",
  summary: "\u4E00\u6B21\u6027\u81EA\u68C0\uFF1ANode \u7248\u672C\u3001Key\u3001\u7F51\u7EDC\u4E0E\u9274\u6743",
  help: `\u7528\u6CD5: mionote doctor [--env prod|test]

\u9010\u9879\u68C0\u67E5\u8FD0\u884C\u73AF\u5883\uFF0C\u8F93\u51FA {ok, checks[]}\u3002\u5168\u90E8\u901A\u8FC7\u9000\u51FA\u7801 0\uFF1B
Key \u7F3A\u5931\u6216\u65E0\u6548\u9000\u51FA\u7801 2\uFF1B\u7F51\u7EDC\u6216\u670D\u52A1\u5F02\u5E38\u9000\u51FA\u7801 3\u3002\u62A5\u544A\u59CB\u7EC8\u8F93\u51FA\u5230 stdout\u3002`,
  options: {},
  async run(ctx, { positionals }) {
    rejectPositionals(positionals, "doctor");
    const checks = [];
    let exitCode = ExitCode.OK;
    const fail = (code) => {
      if (exitCode === ExitCode.OK) exitCode = code;
    };
    const nodeMajor2 = Number(process.versions.node.split(".")[0]);
    const nodeOk = nodeMajor2 >= MIN_NODE_MAJOR;
    checks.push({
      name: "node",
      ok: nodeOk,
      detail: `Node.js ${process.versions.node}`,
      ...!nodeOk && { hint: `\u9700\u8981 Node.js ${MIN_NODE_MAJOR} \u6216\u66F4\u9AD8\u7248\u672C` }
    });
    if (!nodeOk) fail(ExitCode.API);
    checks.push({ name: "env", ok: true, detail: `${ctx.env} \u2192 ${ctx.baseUrl}` });
    try {
      const key = ctx.requireKey();
      checks.push({ name: "apiKey", ok: true, detail: `${maskKey(key.key)}\uFF08\u6765\u6E90: ${key.source}\uFF09` });
      try {
        const groups2 = await ctx.client(key).get("/api/open/v1/groups");
        checks.push({ name: "api", ok: true, detail: `\u8FDE\u63A5\u6B63\u5E38\uFF0C\u5171 ${groups2?.length ?? 0} \u4E2A\u5206\u7EC4` });
      } catch (e) {
        const err = e instanceof CliError ? e : new CliError(ExitCode.API, String(e));
        checks.push({ name: "api", ok: false, detail: err.message, hint: err.hint });
        fail(err.exitCode);
      }
    } catch (e) {
      const err = e;
      checks.push({ name: "apiKey", ok: false, detail: err.message, hint: err.hint });
      fail(ExitCode.AUTH);
    }
    return {
      data: { ok: exitCode === ExitCode.OK, version: VERSION, channel: CHANNEL, checks },
      exitCode
    };
  }
};

// packages/cli/src/dates.ts
var BEIJING_OFFSET_MS = 8 * 60 * 60 * 1e3;
var DAY_MS = 24 * 60 * 60 * 1e3;
var ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;
var LAST_N_DAYS = /^last-(\d{1,3})d$/;
var RANGE_NAMES = [
  "today",
  "yesterday",
  "this-week",
  "last-week",
  "this-month",
  "last-month",
  "last-<N>d"
];
function beijingToday(now) {
  const shifted = new Date(now.getTime() + BEIJING_OFFSET_MS);
  return new Date(Date.UTC(shifted.getUTCFullYear(), shifted.getUTCMonth(), shifted.getUTCDate()));
}
function addDays(day, days) {
  return new Date(day.getTime() + days * DAY_MS);
}
function startOfWeek(day) {
  const weekday = (day.getUTCDay() + 6) % 7;
  return addDays(day, -weekday);
}
function format(day) {
  return day.toISOString().slice(0, 10);
}
function parseIsoDate(value, option) {
  if (!ISO_DATE.test(value)) {
    throw usageError(`--${option} \u683C\u5F0F\u4E0D\u5BF9: ${value}`, "\u7528 YYYY-MM-DD\u3001today \u6216 yesterday");
  }
  const [y, m, d] = value.split("-").map(Number);
  const day = new Date(Date.UTC(y, m - 1, d));
  if (day.getUTCFullYear() !== y || day.getUTCMonth() !== m - 1 || day.getUTCDate() !== d) {
    throw usageError(`--${option} \u4E0D\u662F\u6709\u6548\u65E5\u671F: ${value}`);
  }
  return day;
}
function parseDayValue(value, option, now) {
  const today = beijingToday(now);
  if (value === "today") return today;
  if (value === "yesterday") return addDays(today, -1);
  return parseIsoDate(value, option);
}
function resolveNamedRange(name, now) {
  const today = beijingToday(now);
  const y = today.getUTCFullYear();
  const m = today.getUTCMonth();
  let start;
  let end;
  switch (name) {
    case "today":
      start = end = today;
      break;
    case "yesterday":
      start = end = addDays(today, -1);
      break;
    case "this-week":
      start = startOfWeek(today);
      end = today;
      break;
    case "last-week":
      start = addDays(startOfWeek(today), -7);
      end = addDays(start, 6);
      break;
    case "this-month":
      start = new Date(Date.UTC(y, m, 1));
      end = today;
      break;
    case "last-month":
      start = new Date(Date.UTC(y, m - 1, 1));
      end = new Date(Date.UTC(y, m, 0));
      break;
    default: {
      const match = LAST_N_DAYS.exec(name);
      const n = match ? Number(match[1]) : 0;
      if (n < 1 || n > 366) {
        throw usageError(`\u672A\u77E5\u7684 --range: ${name}`, `\u53EF\u9009\u503C: ${RANGE_NAMES.join(" / ")}\uFF08N \u4E3A 1-366\uFF09`);
      }
      start = addDays(today, -(n - 1));
      end = today;
    }
  }
  return { start: format(start), end: format(end), label: name };
}
function resolveDateRange(input, now = /* @__PURE__ */ new Date()) {
  if (input.range !== void 0) {
    if (input.since !== void 0 || input.until !== void 0) {
      throw usageError("--range \u4E0D\u80FD\u548C --since / --until \u540C\u65F6\u4F7F\u7528");
    }
    return resolveNamedRange(input.range, now);
  }
  const start = input.since === void 0 ? void 0 : parseDayValue(input.since, "since", now);
  const end = input.until === void 0 ? void 0 : parseDayValue(input.until, "until", now);
  if (start && end && start.getTime() > end.getTime()) {
    throw usageError(`--since ${format(start)} \u665A\u4E8E --until ${format(end)}`);
  }
  return {
    start: start && format(start),
    end: end && format(end)
  };
}

// packages/cli/src/groups.ts
var UNGROUPED = { id: -1, name: "\u672A\u5206\u7EC4" };
var UNGROUPED_ALIASES = /* @__PURE__ */ new Set(["-1", "ungrouped", "\u672A\u5206\u7EC4"]);
var MAX_LISTED = 30;
function isUngroupedAlias(input) {
  return UNGROUPED_ALIASES.has(input.trim().toLowerCase());
}
function describe(groups2) {
  const shown = groups2.slice(0, MAX_LISTED).map((g) => `${g.id}:${g.name}`);
  const more = groups2.length > MAX_LISTED ? ` \u7B49 ${groups2.length} \u4E2A` : "";
  return shown.join("\uFF0C") + more;
}
function resolveGroup(input, groups2) {
  const value = input.trim();
  if (!value) throw usageError("--group \u4E0D\u80FD\u4E3A\u7A7A");
  if (isUngroupedAlias(value)) return UNGROUPED;
  if (/^\d+$/.test(value)) {
    const byId = groups2.find((g) => String(g.id) === value);
    if (byId) return { id: byId.id, name: byId.name };
  }
  const needle = value.toLowerCase();
  const pick = (matches) => {
    if (matches.length === 1) return { id: matches[0].id, name: matches[0].name };
    if (matches.length > 1) {
      throw usageError(`\u5206\u7EC4\u300C${value}\u300D\u5339\u914D\u5230\u591A\u4E2A`, `\u8BF7\u6539\u7528 id \u6307\u5B9A\uFF1A${describe(matches)}`);
    }
    return void 0;
  };
  const exact = groups2.filter((g) => g.name.trim().toLowerCase() === needle);
  const partial = groups2.filter((g) => g.name.toLowerCase().includes(needle));
  const found = pick(exact) ?? pick(partial);
  if (found) return found;
  throw usageError(
    `\u6CA1\u6709\u627E\u5230\u5206\u7EC4\u300C${value}\u300D`,
    groups2.length ? `\u73B0\u6709\u5206\u7EC4\uFF1A${describe(groups2)}` : "\u8BE5\u8D26\u53F7\u8FD8\u6CA1\u6709\u4EFB\u4F55\u5206\u7EC4"
  );
}

// packages/cli/src/output.ts
import { chmodSync as chmodSync2, mkdirSync as mkdirSync2, writeFileSync as writeFileSync2 } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join as join2, resolve } from "node:path";
var MEETING_LIST_FIELDS = [
  "id",
  "title",
  "voiceStartTime",
  "voiceEndTime",
  "duration",
  "createTime",
  "groupId",
  "groupName",
  "isShared",
  "aiStatus",
  "aiState"
];
var AI_STATES = { 0: "pending", 1: "processing", 2: "transcribed", 3: "done" };
function aiStateOf(status) {
  return typeof status === "number" && status in AI_STATES ? AI_STATES[status] : null;
}
function withAiState(record) {
  return { ...record, aiState: aiStateOf(record.aiStatus) };
}
function parseFields(raw, known) {
  if (raw === void 0) return void 0;
  const fields = [...new Set(raw.split(",").map((f) => f.trim()).filter(Boolean))];
  if (fields.length === 0) throw usageError("--fields \u4E0D\u80FD\u4E3A\u7A7A");
  const unknown = fields.filter((f) => !known.includes(f));
  if (unknown.length) {
    throw usageError(`--fields \u542B\u672A\u77E5\u5B57\u6BB5: ${unknown.join(", ")}`, `\u53EF\u9009\u5B57\u6BB5: ${known.join(", ")}`);
  }
  return fields;
}
function projectFields(records, fields) {
  if (!fields) return records;
  return records.map((record) => Object.fromEntries(fields.map((f) => [f, record[f] ?? null])));
}
function compactSegments(segments) {
  return segments.map((raw) => {
    const s = raw ?? {};
    const str = (v) => v === void 0 || v === null || v === "" ? null : String(v);
    return { startTime: str(s.startTime), endTime: str(s.endTime), speakerId: str(s.speakerId), text: String(s.text ?? "") };
  });
}
function resolveOutputPath(value, defaultName, baseTmp = tmpdir()) {
  if (value === "auto") return join2(baseTmp, "mionote", defaultName);
  if (!value.trim()) throw usageError("--output \u4E0D\u80FD\u4E3A\u7A7A", "\u4F20\u6587\u4EF6\u8DEF\u5F84\uFF0C\u6216\u7528 auto \u5199\u5230\u4E34\u65F6\u76EE\u5F55");
  return resolve(value);
}
function writePrivateFile(path, content) {
  try {
    mkdirSync2(dirname(path), { recursive: true, mode: 448 });
    writeFileSync2(path, content, { encoding: "utf8", mode: 384 });
    chmodSync2(path, 384);
  } catch (e) {
    throw new CliError(ExitCode.API, `\u5199\u5165\u6587\u4EF6\u5931\u8D25: ${e.message}`);
  }
}
function toJson(value, pretty) {
  return JSON.stringify(value, null, pretty ? 2 : 0);
}

// packages/cli/src/commands/meetings.ts
var GROUPS_PATH = "/api/open/v1/groups";
var MEETINGS_PATH = "/api/open/v1/meetings";
var MAX_PAGE_SIZE = 100;
var DEFAULT_ALL_MAX = 200;
var TRANSCRIPT_INLINE_LIMIT = 3e4;
function timestamp(now) {
  return new Date(now.getTime() + 8 * 36e5).toISOString().replace(/[-:]/g, "").replace(/\..+$/, "");
}
var groups = {
  path: "groups",
  summary: "\u5206\u7EC4\u5217\u8868\uFF08id / \u540D\u79F0 / \u7EAA\u8981\u6570\uFF09",
  help: `\u7528\u6CD5: mionote groups [--env prod|test] [--pretty]

\u8FD4\u56DE [{id, name, meetingCount}]\u3002meetings list \u7684 --group \u53EF\u4EE5\u76F4\u63A5\u5199\u5206\u7EC4\u540D\uFF0C\u901A\u5E38\u4E0D\u5FC5\u5148\u67E5\u8FD9\u91CC\u3002`,
  options: {},
  async run(ctx, { positionals }) {
    rejectPositionals(positionals, "groups");
    const list = await ctx.client(ctx.requireKey()).get(GROUPS_PATH);
    return ok((list ?? []).map(({ id, name, meetingCount }) => ({ id, name, meetingCount })));
  }
};
async function resolveGroupOption(client, raw) {
  if (raw === void 0) return void 0;
  if (isUngroupedAlias(raw)) return UNGROUPED;
  return resolveGroup(raw, await client.get(GROUPS_PATH) ?? []);
}
var meetingsList = {
  path: "meetings list",
  summary: "\u7EAA\u8981\u5217\u8868\uFF1A\u6309\u65E5\u671F / \u5206\u7EC4 / \u6807\u9898\u5173\u952E\u8BCD\u7B5B\u9009\uFF0C\u6309\u521B\u5EFA\u65F6\u95F4\u5012\u5E8F",
  help: `\u7528\u6CD5: mionote meetings list [\u7B5B\u9009] [\u5206\u9875] [\u8F93\u51FA]

\u7B5B\u9009:
  --range <\u540D\u79F0>          ${RANGE_NAMES.join(" | ")}\uFF08\u5317\u4EAC\u65F6\u95F4\uFF0C\u5468\u4E00\u4E3A\u4E00\u5468\u5F00\u59CB\uFF09
  --since <\u65E5\u671F>          \u8D77\u59CB\u65E5\u671F\uFF08\u542B\uFF09\uFF0CYYYY-MM-DD | today | yesterday
  --until <\u65E5\u671F>          \u7ED3\u675F\u65E5\u671F\uFF08\u542B\uFF09\uFF0C\u540C\u4E0A\uFF1B\u4E0E --range \u4E8C\u9009\u4E00
  --group <id|\u5206\u7EC4\u540D>     \u5206\u7EC4\u540D\u652F\u6301\u7CBE\u786E\u6216\u5305\u542B\u5339\u914D\uFF0C\u591A\u4E2A\u547D\u4E2D\u4F1A\u62A5\u9519\uFF1Bungrouped \u8868\u793A\u672A\u5206\u7EC4
  --keyword <\u8BCD>          \u53EA\u5339\u914D\u6807\u9898\uFF0C\u4E0D\u641C\u6B63\u6587

\u5206\u9875:
  --page <n> --page-size <n>   \u9ED8\u8BA4\u7B2C 1 \u9875\u3001\u6BCF\u9875 20 \u6761\uFF0C\u6BCF\u9875\u4E0A\u9650 ${MAX_PAGE_SIZE}
  --all [--max <n>]            \u81EA\u52A8\u7FFB\u9875\u53D6\u5168\u91CF\uFF0C\u9ED8\u8BA4\u6700\u591A ${DEFAULT_ALL_MAX} \u6761\uFF0C\u4E0A\u9650 1000

\u8F93\u51FA:
  --fields <a,b,...>     \u53EA\u4FDD\u7559\u8FD9\u4E9B\u5B57\u6BB5\uFF1A${MEETING_LIST_FIELDS.join(", ")}
  --output <\u6587\u4EF6|auto>    \u8BB0\u5F55\u5199\u5165\u6587\u4EF6\uFF0Cstdout \u53EA\u56DE\u6458\u8981\uFF1Bauto \u5199\u5230\u7CFB\u7EDF\u4E34\u65F6\u76EE\u5F55

\u7ED3\u679C\u4E2D\u7684 query \u5B57\u6BB5\u56DE\u663E\u5B9E\u9645\u751F\u6548\u7684\u65E5\u671F\u8303\u56F4\u4E0E\u5206\u7EC4\uFF0C\u53EF\u76F4\u63A5\u7528\u6765\u5411\u7528\u6237\u8BF4\u660E\u67E5\u8BE2\u53E3\u5F84\uFF1B
hasMore\uFF08\u7FFB\u9875\uFF09\u6216 truncated\uFF08--all\uFF09\u4E3A true \u8868\u793A\u8FD8\u6709\u8BB0\u5F55\u6CA1\u53D6\u5230\u3002
aiState\uFF1Apending \u5F85\u5904\u7406 / processing \u5904\u7406\u4E2D / transcribed \u539F\u6587\u5DF2\u5C31\u7EEA / done AI \u7EAA\u8981\u5DF2\u751F\u6210\uFF08aiStatus 0\uFF5E3 \u4E3A\u5BF9\u5E94\u6570\u5B57\uFF09\u3002`,
  options: {
    range: { type: "string" },
    since: { type: "string" },
    until: { type: "string" },
    group: { type: "string" },
    keyword: { type: "string" },
    page: { type: "string" },
    "page-size": { type: "string" },
    all: { type: "boolean" },
    max: { type: "string" },
    fields: { type: "string" },
    output: { type: "string" }
  },
  async run(ctx, { values, positionals }) {
    rejectPositionals(positionals, "meetings list");
    const all = values.all === true;
    if (all && values.page !== void 0) throw usageError("--all \u4E0E --page \u4E0D\u80FD\u540C\u65F6\u4F7F\u7528");
    if (!all && values.max !== void 0) throw usageError("--max \u53EA\u80FD\u914D\u5408 --all \u4F7F\u7528");
    const range = resolveDateRange(
      { range: stringOption(values, "range"), since: stringOption(values, "since"), until: stringOption(values, "until") },
      ctx.deps.now()
    );
    const fields = parseFields(stringOption(values, "fields"), MEETING_LIST_FIELDS);
    const pageSize = intOption(values, "page-size", all ? MAX_PAGE_SIZE : 20, { min: 1, max: MAX_PAGE_SIZE });
    const page = intOption(values, "page", 1, { min: 1, max: 1e5 });
    const max = intOption(values, "max", DEFAULT_ALL_MAX, { min: 1, max: 1e3 });
    const keyword = stringOption(values, "keyword")?.trim() || void 0;
    const output = stringOption(values, "output");
    const client = ctx.client(ctx.requireKey());
    const group = await resolveGroupOption(client, stringOption(values, "group"));
    const filters = { keyword, groupId: group?.id, startDate: range.start, endDate: range.end };
    const query = {
      ...range.start || range.end ? { range } : {},
      ...group && { group },
      ...keyword && { keyword }
    };
    let result;
    let records;
    if (all) {
      records = [];
      let total = 0;
      for (let p = 1; ; p++) {
        const data = await client.get(MEETINGS_PATH, { page: p, pageSize, ...filters });
        const batch = data?.records ?? [];
        total = data?.total ?? 0;
        records.push(...batch);
        if (batch.length === 0 || records.length >= total || records.length >= max) break;
      }
      records = records.slice(0, max);
      result = { query, total, fetched: records.length, truncated: records.length < total };
    } else {
      const data = await client.get(MEETINGS_PATH, { page, pageSize, ...filters });
      records = data?.records ?? [];
      const total = data?.total ?? 0;
      result = { query, total, page, pageSize, hasMore: page * pageSize < total };
    }
    const projected = projectFields(records.map(withAiState), fields);
    if (output === void 0) return ok({ ...result, records: projected });
    const path = resolveOutputPath(output, `meetings-${timestamp(ctx.deps.now())}.json`, ctx.deps.tmpDir);
    writePrivateFile(path, toJson(projected, true));
    return ok({ ...result, saved: path, count: projected.length });
  }
};
var meetingsGet = {
  path: "meetings get",
  summary: "\u5355\u6761\u7EAA\u8981\u8BE6\u60C5\uFF1AAI \u6458\u8981 / \u8981\u70B9 / \u7ED3\u8BBA + \u7528\u6237\u7B14\u8BB0 + \u53D1\u8A00\u4EBA",
  help: `\u7528\u6CD5: mionote meetings get <\u7EAA\u8981id> [--env prod|test] [--pretty]

\u8FD4\u56DE\u57FA\u672C\u4FE1\u606F\u3001AI \u7EAA\u8981\uFF08aiSummary / aiKeyPoint / aiConclusion\uFF0CaiState=done \u65F6\u5B8C\u6574\uFF09\u3001
\u7528\u6237\u7B14\u8BB0\uFF08userMeetingNoteTitle / userMeetingNote\uFF09\u3001\u53D1\u8A00\u4EBA\uFF08speakers \u4E3A\u663E\u793A\u540D\u9017\u53F7\u5206\u9694 / speakerCount\uFF09\u3002\u4E0D\u542B\u8F6C\u5199\u539F\u6587\u3002`,
  options: {},
  async run(ctx, { positionals }) {
    const id = requireMeetingId(positionals, "meetings get");
    const detail = await ctx.client(ctx.requireKey()).get(`${MEETINGS_PATH}/${id}`);
    return ok(detail ? withAiState(detail) : detail);
  }
};
function saveTranscript(data, format2, path, autoSaved) {
  const content = format2 === "text" ? data.text ?? "" : toJson(data.segments ?? [], true);
  writePrivateFile(path, content);
  return {
    id: data.id,
    title: data.title,
    aiStatus: data.aiStatus,
    aiState: aiStateOf(data.aiStatus),
    speakerCount: data.speakerCount,
    format: format2,
    saved: path,
    ...format2 === "text" ? { chars: content.length } : { segments: (data.segments ?? []).length },
    ...autoSaved && {
      autoSaved: true,
      note: `\u5185\u5BB9\u8D85\u8FC7 ${TRANSCRIPT_INLINE_LIMIT} \u5B57\uFF0C\u5DF2\u81EA\u52A8\u5199\u5165\u6587\u4EF6\uFF0C\u8BF7\u5206\u6BB5\u8BFB\u53D6`
    }
  };
}
var meetingsTranscript = {
  path: "meetings transcript",
  summary: "\u8F6C\u5F55\u539F\u6587\uFF08\u8BF4\u8BDD\u4EBA\u5206\u79BB\u9010\u6BB5\u8F6C\u5199\uFF09",
  help: `\u7528\u6CD5: mionote meetings transcript <\u7EAA\u8981id> [--format segments|text] [--output <\u6587\u4EF6|auto>]

  --format segments   \u9ED8\u8BA4\uFF0C[{startTime, endTime, speakerId, text}]\uFF08\u79D2\uFF09\uFF0C\u9002\u5408\u5F15\u7528\u539F\u8BDD\u3001\u6309\u53D1\u8A00\u4EBA\u5206\u6790\uFF1B
                      speakerId \u662F\u8BF4\u8BDD\u4EBA\u663E\u793A\u540D\uFF08\u7528\u6237\u6539\u8FC7\u540D\u5C31\u662F\u6539\u540E\u7684\u540D\u5B57\uFF09
  --format text       \u5B8C\u6574\u7EAF\u6587\u672C\uFF08"\u53D1\u8A00\u4EBA1:\\n..."\uFF09\uFF0C\u9002\u5408\u6574\u4F53\u91CD\u65B0\u603B\u7ED3
  --output <\u6587\u4EF6|auto> \u5199\u5165\u6587\u4EF6\uFF08\u6743\u9650 0600\uFF09\uFF0Cstdout \u53EA\u56DE\u6458\u8981\uFF1Bauto \u5199\u5230\u7CFB\u7EDF\u4E34\u65F6\u76EE\u5F55

\u672A\u6307\u5B9A --output \u65F6\uFF0C\u5185\u5BB9\u8D85\u8FC7 ${TRANSCRIPT_INLINE_LIMIT} \u5B57\u4F1A\u81EA\u52A8\u5199\u5165\u4E34\u65F6\u6587\u4EF6\u5E76\u8FD4\u56DE\u8DEF\u5F84\u3002
\u8F6C\u5199\u5C1A\u672A\u751F\u6210\u65F6\u9000\u51FA\u7801 4\u3002startTime \u53EF\u80FD\u4E3A null\uFF08\u5386\u53F2\u6570\u636E\u672A\u8BB0\u5F55\u65F6\u95F4\u6233\uFF09\u3002`,
  options: {
    format: { type: "string" },
    output: { type: "string" }
  },
  async run(ctx, { values, positionals }) {
    const id = requireMeetingId(positionals, "meetings transcript");
    const format2 = stringOption(values, "format") ?? "segments";
    if (format2 !== "segments" && format2 !== "text") {
      throw usageError(`--format \u53EA\u652F\u6301 segments \u6216 text\uFF0C\u6536\u5230: ${format2}`);
    }
    const output = stringOption(values, "output");
    const ext = format2 === "text" ? "txt" : "json";
    const defaultName = `transcript-${id}-${format2}.${ext}`;
    const raw = await ctx.client(ctx.requireKey()).get(`${MEETINGS_PATH}/${id}/transcript`, { format: format2 });
    const compacted = raw.segments ? { ...raw, segments: compactSegments(raw.segments) } : raw;
    const data = { ...compacted, aiState: aiStateOf(compacted.aiStatus) };
    if (output !== void 0) {
      return ok(saveTranscript(data, format2, resolveOutputPath(output, defaultName, ctx.deps.tmpDir), false));
    }
    const size = format2 === "text" ? (data.text ?? "").length : toJson(data.segments ?? [], false).length;
    if (size > TRANSCRIPT_INLINE_LIMIT) {
      return ok(saveTranscript(data, format2, resolveOutputPath("auto", defaultName, ctx.deps.tmpDir), true));
    }
    return ok(data);
  }
};

// packages/cli/src/index.ts
var version = {
  path: "version",
  summary: "\u7248\u672C\u4FE1\u606F",
  help: "\u7528\u6CD5: mionote version",
  options: {},
  async run() {
    return ok({ version: VERSION, channel: CHANNEL, node: process.versions.node });
  }
};
var COMMANDS = [
  doctor,
  authSet,
  authStatus,
  authLogout,
  groups,
  meetingsList,
  meetingsGet,
  meetingsTranscript,
  version
];
var GLOBAL_HELP = `\u5168\u5C40\u53C2\u6570:
  --env prod|test   \u76EE\u6807\u73AF\u5883\uFF0C\u9ED8\u8BA4 prod\uFF08\u4E5F\u53EF\u8BBE\u73AF\u5883\u53D8\u91CF MIONOTE_ENV\uFF09
  --pretty          \u7F29\u8FDB\u8F93\u51FA JSON
  -h, --help        \u67E5\u770B\u5E2E\u52A9`;
function topHelp() {
  const width = Math.max(...COMMANDS.map((c) => c.path.length));
  const lines = COMMANDS.map((c) => `  ${c.path.padEnd(width)}  ${c.summary}`);
  return `mionote ${VERSION} \u2014 Meet\u5999\u8BB0\u547D\u4EE4\u884C\uFF1A\u67E5\u8BE2\u672C\u4EBA\u7684\u4F1A\u8BAE\u7EAA\u8981\u3001AI \u6458\u8981\u4E0E\u8F6C\u5F55\u539F\u6587

\u7528\u6CD5: mionote <\u547D\u4EE4> [\u53C2\u6570]

\u547D\u4EE4:
${lines.join("\n")}

${GLOBAL_HELP}

API Key: \u5728 App\u300C\u6211\u7684 \u2192 \u5999\u8BB0 Skill\u300D\u751F\u6210\uFF1B\u4F18\u5148\u8BFB\u73AF\u5883\u53D8\u91CF MIONOTE_API_KEY\uFF0C\u5176\u6B21 mionote auth set \u4FDD\u5B58\u7684\u51ED\u8BC1\u6587\u4EF6\u3002
\u8F93\u51FA: \u6210\u529F\u65F6 stdout \u8F93\u51FA JSON\uFF1B\u5931\u8D25\u65F6 stderr \u8F93\u51FA {"error","hint","exitCode"}\u3002
\u9000\u51FA\u7801: 0 \u6210\u529F / 1 \u53C2\u6570\u9519\u8BEF / 2 Key \u672A\u914D\u7F6E\u6216\u65E0\u6548 / 3 \u63A5\u53E3\u3001\u7F51\u7EDC\u6216\u6587\u4EF6\u9519\u8BEF / 4 \u6570\u636E\u672A\u5C31\u7EEA`;
}
function groupHelp(group) {
  const subs = COMMANDS.filter((c) => c.path.startsWith(`${group} `));
  return `\u7528\u6CD5: mionote ${group} <${subs.map((c) => c.path.split(" ")[1]).join("|")}> [\u53C2\u6570]

${subs.map((c) => `  ${c.path.padEnd(22)}${c.summary}`).join("\n")}

\u6267\u884C mionote ${group} <\u5B50\u547D\u4EE4> --help \u67E5\u770B\u8BE6\u7EC6\u7528\u6CD5`;
}
function commandHelp(command) {
  return `${command.help}

${GLOBAL_HELP}`;
}
function matchCommand(argv) {
  for (const command of [...COMMANDS].sort((a, b) => b.path.length - a.path.length)) {
    const tokens = command.path.split(" ");
    if (tokens.every((t, i) => argv[i] === t)) return { command, rest: argv.slice(tokens.length) };
  }
  return { rest: argv };
}
var isGroup = (name) => name !== void 0 && COMMANDS.some((c) => c.path.startsWith(`${name} `));
function printError(deps2, error) {
  deps2.stderr(`${toJson({ error: error.message, ...error.hint && { hint: error.hint }, exitCode: error.exitCode }, false)}
`);
  return error.exitCode;
}
async function run(argv, deps2) {
  const [first] = argv;
  if (first === void 0 || first === "help" || first === "--help" || first === "-h") {
    const target = first === "help" ? matchCommand(argv.slice(1)).command : void 0;
    if (target) deps2.stdout(`${commandHelp(target)}
`);
    else if (first === "help" && isGroup(argv[1])) deps2.stdout(`${groupHelp(argv[1])}
`);
    else deps2.stdout(`${topHelp()}
`);
    return ExitCode.OK;
  }
  if (first === "--version" || first === "-v") argv = ["version", ...argv.slice(1)];
  const { command, rest } = matchCommand(argv);
  if (!command) {
    if (isGroup(first)) {
      const sub = argv[1];
      if (sub === void 0 || sub === "--help" || sub === "-h") {
        deps2.stdout(`${groupHelp(first)}
`);
        return ExitCode.OK;
      }
      return printError(deps2, new CliError(ExitCode.USAGE, `\u672A\u77E5\u5B50\u547D\u4EE4: ${first} ${sub}`, `\u6267\u884C mionote ${first} --help`));
    }
    return printError(deps2, new CliError(ExitCode.USAGE, `\u672A\u77E5\u547D\u4EE4: ${first}`, "\u6267\u884C mionote --help \u67E5\u770B\u5168\u90E8\u547D\u4EE4"));
  }
  try {
    const parsed = parseCommandArgs(rest, command.options, command.path);
    if (parsed.values.help === true) {
      deps2.stdout(`${commandHelp(command)}
`);
      return ExitCode.OK;
    }
    const ctx = createContext(parsed.values, deps2);
    const result = await command.run(ctx, parsed);
    deps2.stdout(`${toJson(result.data, ctx.pretty)}
`);
    return result.exitCode;
  } catch (e) {
    if (e instanceof CliError) return printError(deps2, e);
    return printError(deps2, new CliError(ExitCode.API, `\u672A\u9884\u671F\u7684\u9519\u8BEF: ${e?.message ?? String(e)}`));
  }
}

// packages/cli/src/bin.ts
var PIPE_READ_TIMEOUT_MS = 6e4;
var BRACKETED_PASTE = /\u001b\[20[01]~/g;
function readFromPipe() {
  return new Promise((resolve2, reject) => {
    const chunks = [];
    const timer = setTimeout(() => {
      process.stdin.pause();
      reject(new CliError(ExitCode.USAGE, "\u7B49\u5F85\u6807\u51C6\u8F93\u5165\u8D85\u65F6", `\u7528\u7BA1\u9053\u4F20\u5165 Key\uFF1Aprintf '%s' "$KEY" | mionote auth set`));
    }, PIPE_READ_TIMEOUT_MS);
    process.stdin.on("data", (chunk) => chunks.push(chunk));
    process.stdin.on("end", () => {
      clearTimeout(timer);
      resolve2(Buffer.concat(chunks).toString("utf8"));
    });
    process.stdin.on("error", (e) => {
      clearTimeout(timer);
      reject(e);
    });
  });
}
function readHidden(prompt) {
  const stdin = process.stdin;
  process.stderr.write(prompt);
  stdin.setRawMode(true);
  stdin.setEncoding("utf8");
  stdin.resume();
  return new Promise((resolve2, reject) => {
    let value = "";
    const finish = (error) => {
      stdin.setRawMode(false);
      stdin.pause();
      stdin.off("data", onData);
      process.stderr.write("\n");
      if (error) reject(error);
      else resolve2(value.replace(BRACKETED_PASTE, ""));
    };
    const onData = (chunk) => {
      for (const ch of chunk) {
        if (ch === "\r" || ch === "\n") return finish();
        if (ch === "") return finish(new CliError(ExitCode.USAGE, "\u5DF2\u53D6\u6D88"));
        if (ch === "\x7F" || ch === "\b") value = value.slice(0, -1);
        else value += ch;
      }
    };
    stdin.on("data", onData);
  });
}
var deps = {
  envVars: process.env,
  now: () => /* @__PURE__ */ new Date(),
  fetchImpl: (...args) => fetch(...args),
  tmpDir: tmpdir2(),
  stdout: (text) => process.stdout.write(text),
  stderr: (text) => process.stderr.write(text),
  readSecret: (prompt) => process.stdin.isTTY ? readHidden(prompt) : readFromPipe()
};
var nodeMajor = Number(process.versions.node.split(".")[0]);
if (nodeMajor < MIN_NODE_MAJOR || typeof fetch !== "function") {
  process.stderr.write(
    `${JSON.stringify({ error: `\u9700\u8981 Node.js ${MIN_NODE_MAJOR} \u6216\u66F4\u9AD8\u7248\u672C\uFF0C\u5F53\u524D ${process.versions.node}`, exitCode: ExitCode.API })}
`
  );
  process.exitCode = ExitCode.API;
} else {
  run(process.argv.slice(2), deps).then((code) => {
    process.exitCode = code;
  });
}
