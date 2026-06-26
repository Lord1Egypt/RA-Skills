import { spawn } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

const DATA_DIR = path.join(os.homedir(), ".grinders-farm");
const PID_FILE = path.join(DATA_DIR, "image-server.pid");
const INFO_FILE = path.join(DATA_DIR, "image-server.json");

function isProcessRunning(pid: number): boolean {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function removeStalePidFile(): void {
  if (!fs.existsSync(PID_FILE)) return;
  const raw = fs.readFileSync(PID_FILE, "utf8").trim();
  const pid = Number.parseInt(raw, 10);
  if (!Number.isFinite(pid) || !isProcessRunning(pid)) {
    try {
      fs.unlinkSync(PID_FILE);
    } catch {
      /* ignore */
    }
    try {
      if (fs.existsSync(INFO_FILE)) fs.unlinkSync(INFO_FILE);
    } catch {
      /* ignore */
    }
  }
}

function tryGetBaseUrlFromInfoFile(): string | null {
  if (!fs.existsSync(INFO_FILE)) return null;
  try {
    const raw = JSON.parse(fs.readFileSync(INFO_FILE, "utf8")) as { baseUrl?: unknown };
    return typeof raw.baseUrl === "string" && raw.baseUrl.trim() ? raw.baseUrl.trim() : null;
  } catch {
    return null;
  }
}

export async function startImageServerAtRoot(
  gameRoot: string,
  preferredPort: number,
): Promise<{ success: boolean; message: string }> {
  removeStalePidFile();

  if (fs.existsSync(PID_FILE)) {
    const pid = Number.parseInt(fs.readFileSync(PID_FILE, "utf8").trim(), 10);
    if (Number.isFinite(pid) && isProcessRunning(pid)) {
      const baseUrl = tryGetBaseUrlFromInfoFile();
      return { success: true, message: `本地图片服务已在运行 (PID ${pid})${baseUrl ? ` · ${baseUrl}` : ""}` };
    }
  }

  const worker = path.join(gameRoot, "src/adapters/image-server.ts");
  const port = Number.isFinite(preferredPort) && preferredPort > 0 ? preferredPort : 18931;
  const child = spawn("npx", ["tsx", worker, String(port)], {
    cwd: gameRoot,
    detached: true,
    stdio: "ignore",
  });
  child.unref();

  for (let i = 0; i < 60; i++) {
    await new Promise<void>((resolve) => setTimeout(resolve, 50));
    if (fs.existsSync(INFO_FILE)) {
      const pid = fs.existsSync(PID_FILE) ? fs.readFileSync(PID_FILE, "utf8").trim() : "?";
      const baseUrl = tryGetBaseUrlFromInfoFile();
      return {
        success: true,
        message: `本地图片服务已启动 (PID ${pid})${baseUrl ? ` · ${baseUrl}` : ""}`,
      };
    }
  }

  return {
    success: false,
    message: "本地图片服务未就绪：请确认 gameRoot 指向 grinders-farm 仓库且可运行 npx tsx src/adapters/image-server.ts",
  };
}
