import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { readFile, readdir, stat } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadApiConfig, readKey, readLedger } from "./api-image.mjs";
import { LOVART_DEFAULT_MODEL } from "./lovart.mjs";
import { PLAYWRIGHT_BROWSER_FAILURE } from "./batch-policy.mjs";
import { childEnv } from "./scoped-env.mjs";
import { STDIO_DISCARD, STDIO_PIPE } from "./stdio-modes.mjs";

export const ENGINES = ["codex", "grok", "gemini", "jimeng", "muse", "lovart", "api"];
export const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
export const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
export const SMOKE_CACHE = process.env.IMAGE_GEN_SMOKE_CACHE || path.join(homedir(), ".config", "imagegen-swarm", "smoke-last.json");

function engineOffFile(engine, env) {
  const dirs = env.IMAGE_GEN_ENGINE_OFF ? [env.IMAGE_GEN_ENGINE_OFF] : ["imagegen-swarm", "image-gen"].map(name =>
    path.join(homedir(), ".config", name, "engine-off"));
  return dirs.map(dir => path.join(dir, engine)).find(existsSync);
}

export function turnedOff(engine, env = process.env) {
  return Boolean(engineOffFile(engine, env));
}

export async function readEngineOff(engine, env = process.env) {
  const file = engineOffFile(engine, env);
  if (!file) return null;
  let reason = "";
  try {
    if ((await stat(file)).isFile()) {
      reason = (await readFile(file, "utf8")).replaceAll(homedir(), "~")
        .replace(/\s+/g, " ").replace(/[\x00-\x1f\x7f]/g, "").trim().slice(0, 200);
    }
  } catch {
    // An unreadable marker still disables generation.
  }
  return { file, displayPath: file.replace(homedir(), "~"), reason };
}

export function isZh(env = process.env) {
  return /^zh/i.test(env.LC_ALL || env.LC_MESSAGES || env.LANG || Intl.DateTimeFormat().resolvedOptions().locale);
}

export function run(bin, args, { timeout = 25000, env = childEnv(), signal } = {}) {
  return new Promise(resolve => {
    let stdout = "", stderr = "", timedOut = false;
    if (signal?.aborted) return resolve({ code: null, stdout, stderr, timedOut });
    const grouped = process.platform !== "win32";
    const child = spawn(bin, args, {
      stdio: [STDIO_DISCARD, STDIO_PIPE, STDIO_PIPE], detached: grouped, env,
    });
    const kill = () => {
      try {
        if (grouped) process.kill(-child.pid, "SIGKILL");
        else if (child.pid) {
          const task = spawn("taskkill.exe", ["/pid", String(child.pid), "/t", "/f"], { stdio: "ignore", windowsHide: true });
          task.once("error", () => child.kill("SIGKILL"));
          task.unref();
        }
      } catch {}
      child.stdout.destroy();
      child.stderr.destroy();
    };
    const timer = setTimeout(() => {
      timedOut = true;
      kill();
    }, timeout);
    signal?.addEventListener("abort", kill, { once: true });
    child.stdout.on("data", data => { stdout += data; });
    child.stderr.on("data", data => { stderr += data; });
    const finish = code => {
      clearTimeout(timer);
      signal?.removeEventListener("abort", kill);
      resolve({ code, stdout, stderr, timedOut });
    };
    child.once("error", () => finish(-1));
    child.once("close", finish);
  });
}

export function lastJson(stdout) {
  for (const line of stdout.trim().split(/\r?\n/).reverse()) {
    try {
      const parsed = JSON.parse(line);
      if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) return parsed;
    } catch {}
  }
  return null;
}

async function resolveCodex(signal, env) {
  if (env.CODEX_BIN) return existsSync(env.CODEX_BIN) ? env.CODEX_BIN : null;
  if ((await run("codex", ["--version"], { signal, env })).code === 0) return "codex";
  const app = "Applications/Codex.app/Contents/Resources/codex";
  for (const exe of [path.join("/", app), path.join(homedir(), app)]) {
    if (existsSync(exe)) return exe;
  }
  if (process.platform !== "win32") return null;
  const dir = path.join(homedir(), "AppData", "Local", "OpenAI", "Codex", "bin");
  let best = null, latest = 0;
  for (const entry of await readdir(dir).catch(() => [])) {
    const file = path.join(dir, entry, "codex.exe");
    const info = await stat(file).catch(() => null);
    if (info && info.mtimeMs > latest) { best = file; latest = info.mtimeMs; }
  }
  return best;
}

const good = (reason, extra) => ({ loggedIn: true, reason, ...extra });
const bad = reason => ({ loggedIn: false, reason });

export async function probeEngine(engine, { scripts = SCRIPT_DIR, env = childEnv(), signal } = {}) {
  const marker = await readEngineOff(engine, env);
  const login = await probeLogin(engine, { scripts, env, signal });
  if (!marker) return login;
  const zh = isZh(env);
  const status = login.loggedIn
    ? (zh ? "已登录但被关闭" : "Logged in, but disabled")
    : (zh ? "未登录且被关闭" : "Not logged in, and disabled");
  const details = [status + " (" + marker.displayPath + ")."];
  if (marker.reason) details.push((zh ? "原因: " : "reason: ") + marker.reason);
  if (!login.loggedIn) details.push(login.reason);
  details.push(zh ? "删掉或移走这个文件即可恢复" : "Remove or move this file to re-enable.");
  return {
    ...login, loggedIn: false, disabled: true, accountLoggedIn: login.loggedIn,
    markerPath: marker.displayPath, markerReason: marker.reason, reason: details.join(" "),
  };
}

async function probeLogin(engine, { scripts, env, signal }) {
  const zh = isZh(env);
  const probe = (bin, args) => run(bin, args, { env, signal });
  switch (engine) {
    case "codex": {
      const codex = await resolveCodex(signal, env);
      const auth = path.join(env.CODEX_HOME || path.join(homedir(), ".codex"), "auth.json");
      if (!codex) return bad("Codex CLI missing. See SETUP.md.");
      return existsSync(auth) ? good("Codex auth.json exists.", { codex }) : bad("Codex auth.json missing. Run codex login.");
    }
    case "grok": {
      const { code, stdout, stderr } = await probe("grok", ["models"]);
      const out = stdout + "\n" + stderr;
      return code === 0 && !/not authenticated/i.test(out) && /grok-[\w.-]+/i.test(out)
        ? good("Grok lists models.") : bad("Grok login or model listing failed. Check the CLI and run grok login --device-code.");
    }
    case "gemini": {
      const agy = env.AGY_BIN || path.join(homedir(), ".local", "bin", "agy");
      const { code, stdout, stderr } = await probe(agy, ["models"]);
      const out = stdout + "\n" + stderr;
      if (code === -1 || /\bENOENT\b|(?:^|[\s:])(?:agy|command):?\s+not found\b|\bnot found:\s*agy\b/i.test(out)) {
        return bad(zh ? "没安装 Antigravity CLI（agy），参考 SETUP.md" : "Antigravity CLI (agy) is not installed. See SETUP.md.");
      }
      if (/please\s+sign\s+in|sign\s+in\s+(?:required|again)|not\s+signed\s+in|login\s+expired|not\s+logged\s+in|unauthenticated/i.test(out)) {
        return bad(zh ? "登录过期，运行 agy 重新登录" : "Gemini login expired; run agy to sign in again.");
      }
      return code === 0 && /gemini-[\w.-]+/i.test(out)
        ? good("Antigravity lists Gemini models.", { agy })
        : bad(zh ? "Gemini 模型列表查询失败。" : "Gemini model listing failed.");
    }
    case "jimeng": {
      const name = process.platform === "win32" ? "dreamina.exe" : "dreamina";
      const dreams = [env.DREAMINA_INSTALL_DIR, path.join(homedir(), "bin"), path.join(homedir(), ".local", "bin")];
      const bin = dreams.filter(Boolean).map(dir => path.join(dir, name)).find(existsSync) || "dreamina";
      const { code, stdout } = await probe(bin, ["user_credit"]);
      const credits = stdout.match(/"total_credit"\s*:\s*(\d+)/)?.[1];
      return code === 0 && credits !== undefined
        ? good("Dreamina credit balance: " + credits + ".") : bad("Dreamina credit check failed. See SETUP.md and run dreamina login.");
    }
    case "muse": {
      const python = env.PYTHON || PY;
      const { code, stdout, stderr } = await probe(python, [path.join(scripts, "muse-image.py"), "--list-chats"]);
      const report = lastJson(stdout);
      if (code === 0 && report?.status === "ok" && Array.isArray(report.chats)) {
        return good("Muse lists side chats.", { remoteDir: report.remote_dir });
      }
      const out = [stdout, stderr, report?.reason, report?.error_kind].join("\n");
      const command = (/[^\w./:-]/.test(python) ? JSON.stringify(python) : python) + " -m ";
      const install = command + "playwright install chromium";
      const setup = command + "pip install playwright && " + install;
      const browserFailure = PLAYWRIGHT_BROWSER_FAILURE.test(out) || /\bspawn\b[^\r\n]{0,200}\b(?:ENOENT|EACCES)\b/i.test(out);
      if (code === -1 || /Python runtime not installed|ModuleNotFoundError:\s*No module named ['"]playwright['"]/i.test(out)
          || (!browserFailure && /\bENOENT\b/i.test(out))) {
        return bad(zh ? "缺少 Python 或 Playwright，安装 Python 后运行 " + setup
          : "Python or Playwright is missing. With Python installed, run " + setup);
      }
      const lockedProfile = /profile.*(?:lock|in use|already running)|ProcessSingleton|SingletonLock|user data directory is already in use/i.test(out);
      if (lockedProfile) return bad(zh ? "Muse 浏览器配置正在使用或已锁定。" : "Muse browser profile is in use or locked.");
      if (browserFailure) {
        return bad(zh ? "Playwright 浏览器没装好/损坏，运行 " + install
          : "Playwright browser is missing or broken; run " + install);
      }
      if (/Muse profile directory does not exist|看不到消息输入框|\bnot logged in\b|\blog[ -]?in\b/i.test(out)) {
        return bad(zh ? "Muse 未登录，运行 muse-image.py --login" : "Muse is not logged in. Run muse-image.py --login.");
      }
      return bad(zh ? "Muse 侧聊天列表查询失败。" : "Muse side chat listing failed.");
    }
    case "lovart": {
      const { code, stdout } = await probe(process.execPath, [path.join(scripts, "lovart.mjs"), "--query-mode", "--json"]);
      const report = lastJson(stdout);
      if (code !== 0 || report?.status !== "ok" || !["fast", "unlimited"].includes(report.billing_mode)) {
        return bad("Lovart billing query failed. Check the wrapper or API credentials in SETUP.md.");
      }
      const free = report.billing_mode === "unlimited" && Array.isArray(report.unlimited_models)
        && report.unlimited_models.includes(LOVART_DEFAULT_MODEL);
      return good("Lovart credentials accepted.", { billingMode: report.billing_mode, free });
    }
    case "api": {
      try {
        const api = loadApiConfig();
        if (!api) return bad("Paid API line is off. Configure api.json as described in SETUP.md.");
        const key = readKey(api);
        const openai = api.provider === "openai";
        const url = api.base + (openai ? "/v1/models" : "/v1beta/models");
        const headers = openai ? { Authorization: "Bearer " + key } : { "x-goog-api-key": key };
        const result = await fetch(url, { headers, signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(20000)]) : AbortSignal.timeout(20000) });
        if (!result.ok) return bad("API model listing failed (HTTP " + result.status + "). Check api.json and the key.");
        const spent = readLedger();
        const budget = spent.month + ": " + spent.images + " images, about $" + spent.usd
          + " of $" + api.budgetMonth + " monthly, $" + api.budgetBatch + " per batch and $" + api.price + " per image.";
        return good("Paid API key accepted by the free model list.", { keyEnv: api.keyEnv, budget });
      } catch {
        return bad("API model listing unavailable. Check api.json, the key and connectivity.");
      }
    }
    default: throw new Error("Unknown engine: " + engine);
  }
}

export async function readSmokeCache(file = SMOKE_CACHE) {
  try {
    const parsed = JSON.parse(await readFile(file, "utf8"));
    return parsed?.engines ?? {};
  } catch { return {}; }
}

export function readinessState(loggedIn, latest, now = Date.now()) {
  if (!loggedIn) return "NOT READY ❌";
  const age = now - Date.parse(latest?.time);
  if (latest?.result === "PASS" && age >= 0 && age < 86400000) {
    return "READY ✅ (实测 " + latest.time + ")";
  }
  return "LOGGED IN, UNTESTED";
}
