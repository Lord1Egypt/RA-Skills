import { spawn, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import type { CommandResult } from "./game/types.js";

/** Project root (grinders-farm repo), resolved from this file under `src/`. */
export const PROJECT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const DATA_DIR = path.join(os.homedir(), ".grinders-farm");
export const AUTO_PID_FILE = path.join(DATA_DIR, "auto.pid");
export const AUTO_CONFIG_FILE = path.join(DATA_DIR, "auto.config.json");

function isProcessRunning(pid: number): boolean {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function listRunningAutoWorkerPids(): number[] {
  try {
    const ps = spawnSync("ps", ["-Ao", "pid,command"], {
      encoding: "utf8",
      maxBuffer: 4 * 1024 * 1024,
    });
    const out = (ps.stdout ?? "").trim();
    if (!out) return [];
    const pids = new Set<number>();
    for (const line of out.split("\n")) {
      if (!line.includes("auto-worker.ts") && !line.includes("auto-worker.js")) continue;
      const m = line.trim().match(/^(\d+)\s+/);
      if (!m) continue;
      const pid = parseInt(m[1], 10);
      if (!Number.isFinite(pid) || pid === process.pid) continue;
      pids.add(pid);
    }
    return Array.from(pids.values()).sort((a, b) => a - b);
  } catch {
    return [];
  }
}

function resolveOpenclawBinForWorker(): string | null {
  const fromEnv = process.env.OPENCLAW_BIN?.trim();
  if (fromEnv) return fromEnv;

  const which = spawnSync("sh", ["-lc", "command -v openclaw"], {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
  });
  const fromWhich = (which.stdout ?? "").trim();
  if (fromWhich) return fromWhich;

  const candidates = [
    process.env.OPENCLAW_PATH?.trim(),
    process.env.NVM_BIN ? path.join(process.env.NVM_BIN, "openclaw") : "",
    "/opt/homebrew/bin/openclaw",
    "/usr/local/bin/openclaw",
  ]
    .map((p) => (p ?? "").trim())
    .filter(Boolean);
  for (const p of candidates) {
    try {
      fs.accessSync(p, fs.constants.X_OK);
      return p;
    } catch {
      // keep trying
    }
  }
  return null;
}

function resolveWorkerCommand(gameRoot: string, intervalSec: number): { cmd: string; args: string[] } | null {
  const tsWorker = path.join(gameRoot, "src", "adapters", "auto-worker.ts");
  if (fs.existsSync(tsWorker)) {
    return { cmd: "npx", args: ["tsx", tsWorker, String(intervalSec)] };
  }

  const distWorker = path.join(gameRoot, "dist", "src", "adapters", "auto-worker.js");
  if (fs.existsSync(distWorker)) {
    return { cmd: process.execPath, args: [distWorker, String(intervalSec)] };
  }

  const srcJsWorker = path.join(gameRoot, "src", "adapters", "auto-worker.js");
  if (fs.existsSync(srcJsWorker)) {
    return { cmd: process.execPath, args: [srcJsWorker, String(intervalSec)] };
  }
  return null;
}

function removeStalePidFile(): void {
  if (!fs.existsSync(AUTO_PID_FILE)) return;
  const raw = fs.readFileSync(AUTO_PID_FILE, "utf8").trim();
  const pid = parseInt(raw, 10);
  if (!Number.isFinite(pid) || !isProcessRunning(pid)) {
    try {
      fs.unlinkSync(AUTO_PID_FILE);
    } catch {
      /* ignore */
    }
    try {
      if (fs.existsSync(AUTO_CONFIG_FILE)) fs.unlinkSync(AUTO_CONFIG_FILE);
    } catch {
      /* ignore */
    }
  }
}

/**
 * 与 `startLocalAuto` 相同，但指定游戏仓库根目录（供 OpenClaw 插件使用，gameRoot 含 `src/adapters/oneshot.ts`）。
 */
export async function startLocalAutoAtRoot(gameRoot: string, intervalSec: number): Promise<CommandResult> {
  removeStalePidFile();

  const runningPids = listRunningAutoWorkerPids();
  if (runningPids.length > 0) {
    return {
      success: false,
      message: `自动推进已在运行中 (PID ${runningPids.join(", ")})。用 "stop" 停止`,
    };
  }

  if (fs.existsSync(AUTO_PID_FILE)) {
    const pid = parseInt(fs.readFileSync(AUTO_PID_FILE, "utf8").trim(), 10);
    if (Number.isFinite(pid) && isProcessRunning(pid)) {
      return { success: false, message: `自动推进已在运行中 (PID ${pid})。用 "stop" 停止` };
    }
  }

  const worker = resolveWorkerCommand(gameRoot, intervalSec);
  if (!worker) {
    return {
      success: false,
      message:
        '自动推进未找到 worker 入口。请确认安装完整（应包含 dist/src/adapters/auto-worker.js），或在源码目录下运行并确保可执行 "npx tsx src/adapters/auto-worker.ts"',
    };
  }
  const resolvedOpenclawBin = resolveOpenclawBinForWorker();
  const child = spawn(worker.cmd, worker.args, {
    cwd: gameRoot,
    detached: true,
    stdio: "ignore",
    env: {
      ...process.env,
      ...(resolvedOpenclawBin ? { OPENCLAW_BIN: resolvedOpenclawBin } : {}),
    },
  });
  child.unref();

  for (let i = 0; i < 50; i++) {
    await new Promise<void>((resolve) => setTimeout(resolve, 50));
    if (fs.existsSync(AUTO_PID_FILE)) {
      const pid = fs.readFileSync(AUTO_PID_FILE, "utf8").trim();
      const human = intervalSec >= 3600 ? `每 ${Math.round(intervalSec / 3600)} 小时` : `每 ${intervalSec} 秒`;
      return {
        success: true,
        message: [
          "🤖 本地自动推进已启动",
          `${human} 推进一天 · 后台 PID ${pid}`,
          "用 \"stop\" 停止；用 \"farm\" 随时查看农场",
        ].join("\n"),
      };
    }
  }

  return {
    success: false,
    message:
      "自动推进进程未在预期时间内就绪。请确认已安装 Node，且本目录可运行：npx tsx src/adapters/auto-worker.ts",
  };
}

export async function startLocalAuto(intervalSec: number): Promise<CommandResult> {
  return startLocalAutoAtRoot(PROJECT_ROOT, intervalSec);
}

export function stopLocalAuto(): CommandResult {
  removeStalePidFile();

  const runningPids = listRunningAutoWorkerPids();
  if (runningPids.length === 0 && !fs.existsSync(AUTO_PID_FILE)) return { success: false, message: "自动推进未在运行" };

  let pidFromFile: number | null = null;
  if (fs.existsSync(AUTO_PID_FILE)) {
    const raw = fs.readFileSync(AUTO_PID_FILE, "utf8").trim();
    const pid = parseInt(raw, 10);
    if (Number.isFinite(pid)) pidFromFile = pid;
  }

  const allPids = new Set<number>(runningPids);
  if (pidFromFile && isProcessRunning(pidFromFile)) allPids.add(pidFromFile);

  if (allPids.size === 0) {
    try {
      if (fs.existsSync(AUTO_PID_FILE)) fs.unlinkSync(AUTO_PID_FILE);
      if (fs.existsSync(AUTO_CONFIG_FILE)) fs.unlinkSync(AUTO_CONFIG_FILE);
    } catch {
      /* ignore */
    }
    return { success: false, message: "自动推进未在运行（进程已结束，已清理）" };
  }

  const failed: Array<{ pid: number; reason: string }> = [];
  for (const pid of allPids) {
    try {
      process.kill(pid, "SIGTERM");
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      failed.push({ pid, reason: msg });
    }
  }

  try {
    fs.unlinkSync(AUTO_PID_FILE);
  } catch {
    /* ignore */
  }
  try {
    if (fs.existsSync(AUTO_CONFIG_FILE)) fs.unlinkSync(AUTO_CONFIG_FILE);
  } catch {
    /* ignore */
  }

  const stopped = Array.from(allPids).filter((pid) => !failed.some((f) => f.pid === pid));
  if (failed.length > 0) {
    return {
      success: false,
      message: `已停止部分自动推进进程（成功: ${stopped.join(", ") || "无"}；失败: ${failed.map((f) => `${f.pid}:${f.reason}`).join("; ")}）`,
    };
  }
  return { success: true, message: `🛑 已停止自动推进 (PID ${stopped.join(", ")} 已结束)` };
}

export function getLocalAutoStatus(): CommandResult {
  removeStalePidFile();

  if (!fs.existsSync(AUTO_PID_FILE)) {
    return { success: true, message: "💤 自动推进: 未运行\n用 \"start\" 启动（固定每 20 分钟推进一天）" };
  }

  const pid = parseInt(fs.readFileSync(AUTO_PID_FILE, "utf8").trim(), 10);
  if (!Number.isFinite(pid) || !isProcessRunning(pid)) {
    return { success: true, message: "💤 自动推进: 未运行（残留文件已忽略）" };
  }

  let intervalHint = "";
  try {
    if (fs.existsSync(AUTO_CONFIG_FILE)) {
      const cfg = JSON.parse(fs.readFileSync(AUTO_CONFIG_FILE, "utf8")) as { intervalSec?: number };
      if (typeof cfg.intervalSec === "number") {
        intervalHint =
          cfg.intervalSec >= 3600
            ? `间隔约 ${Math.round(cfg.intervalSec / 3600)} 小时`
            : `间隔 ${cfg.intervalSec} 秒`;
      }
    }
  } catch {
    /* ignore */
  }

  return {
    success: true,
    message: ["🤖 自动推进: 运行中", `PID ${pid}${intervalHint ? ` · ${intervalHint}` : ""}`, "用 \"stop\" 停止"].join(
      "\n",
    ),
  };
}
