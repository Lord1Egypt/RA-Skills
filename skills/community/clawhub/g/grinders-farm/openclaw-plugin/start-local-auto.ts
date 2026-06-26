/**
 * 不 import ../src/local-auto：插件装在 extensions 时 ../src 不存在。
 */
import { spawn, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

const DATA_DIR = path.join(os.homedir(), ".grinders-farm");
const AUTO_PID_FILE = path.join(DATA_DIR, "auto.pid");
const AUTO_CONFIG_FILE = path.join(DATA_DIR, "auto.config.json");

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
      if (!line.includes("src/adapters/auto-worker.ts")) continue;
      const m = line.trim().match(/^(\d+)\s+/);
      if (!m) continue;
      const pid = parseInt(m[1], 10);
      if (!Number.isFinite(pid)) continue;
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

export async function startLocalAutoAtRoot(
  gameRoot: string,
  intervalSec: number,
): Promise<{ success: boolean; message: string }> {
  removeStalePidFile();
  const runningPids = listRunningAutoWorkerPids();
  if (runningPids.length > 0) {
    return { success: false, message: `自动推进已在运行中 (PID ${runningPids.join(", ")})` };
  }

  if (fs.existsSync(AUTO_PID_FILE)) {
    const pid = parseInt(fs.readFileSync(AUTO_PID_FILE, "utf8").trim(), 10);
    if (Number.isFinite(pid) && isProcessRunning(pid)) {
      return { success: false, message: `自动推进已在运行中 (PID ${pid})` };
    }
  }

  const worker = path.join(gameRoot, "src/adapters/auto-worker.ts");
  const resolvedOpenclawBin = resolveOpenclawBinForWorker();
  const child = spawn("npx", ["tsx", worker, String(intervalSec)], {
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
        message: `本地 auto-worker 已启动 · ${human} · PID ${pid}`,
      };
    }
  }

  return {
    success: false,
    message: "auto-worker 未就绪：请确认 gameRoot 指向 grinders-farm 仓库且可运行 npx tsx src/adapters/auto-worker.ts",
  };
}
