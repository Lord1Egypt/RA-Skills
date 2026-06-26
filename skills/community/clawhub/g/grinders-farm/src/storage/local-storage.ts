import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";
import { FarmState } from "../game/types.js";

const DEFAULT_DIR = path.join(os.homedir(), ".grinders-farm");
const DEFAULT_FILE = "farm.json";
const LOCK_FILE = "farm.lock";
const LOCK_RETRY_MS = 50;
const LOCK_TIMEOUT_MS = 5000;
const LOCK_STALE_MS = 60000;

export class LocalStorage {
  private filePath: string;
  private lockPath: string;

  constructor(dir?: string) {
    const storageDir = dir ?? DEFAULT_DIR;
    if (!fs.existsSync(storageDir)) {
      fs.mkdirSync(storageDir, { recursive: true });
    }
    this.filePath = path.join(storageDir, DEFAULT_FILE);
    this.lockPath = path.join(storageDir, LOCK_FILE);
  }

  load(): FarmState | null {
    try {
      if (!fs.existsSync(this.filePath)) return null;
      const raw = fs.readFileSync(this.filePath, "utf-8");
      return JSON.parse(raw) as FarmState;
    } catch {
      return null;
    }
  }

  save(state: FarmState): void {
    fs.writeFileSync(this.filePath, JSON.stringify(state, null, 2), "utf-8");
  }

  reset(): void {
    if (fs.existsSync(this.filePath)) {
      fs.unlinkSync(this.filePath);
    }
  }

  getPath(): string {
    return this.filePath;
  }

  async withStateLock<T>(fn: () => Promise<T>): Promise<T> {
    const release = await this.acquireLock();
    try {
      return await fn();
    } finally {
      release();
    }
  }

  private async acquireLock(): Promise<() => void> {
    const startedAt = Date.now();
    while (Date.now() - startedAt < LOCK_TIMEOUT_MS) {
      this.cleanupStaleLock();
      try {
        const fd = fs.openSync(this.lockPath, "wx");
        const payload = JSON.stringify({ pid: process.pid, ts: Date.now() });
        fs.writeFileSync(fd, payload, "utf8");
        return () => {
          try {
            fs.closeSync(fd);
          } catch {
            /* ignore */
          }
          try {
            fs.unlinkSync(this.lockPath);
          } catch {
            /* ignore */
          }
        };
      } catch (err) {
        const code = (err as NodeJS.ErrnoException).code;
        if (code !== "EEXIST") throw err;
      }
      await new Promise<void>((resolve) => setTimeout(resolve, LOCK_RETRY_MS));
    }
    throw new Error("获取农场状态锁超时，请稍后重试");
  }

  private cleanupStaleLock(): void {
    if (!fs.existsSync(this.lockPath)) return;
    try {
      const raw = JSON.parse(fs.readFileSync(this.lockPath, "utf8")) as { pid?: unknown; ts?: unknown };
      const pid = typeof raw.pid === "number" ? raw.pid : NaN;
      const ts = typeof raw.ts === "number" ? raw.ts : 0;
      const tooOld = Date.now() - ts > LOCK_STALE_MS;
      const dead = !Number.isFinite(pid) || !this.isPidRunning(pid);
      if (tooOld || dead) fs.unlinkSync(this.lockPath);
    } catch {
      try {
        fs.unlinkSync(this.lockPath);
      } catch {
        /* ignore */
      }
    }
  }

  private isPidRunning(pid: number): boolean {
    try {
      process.kill(pid, 0);
      return true;
    } catch {
      return false;
    }
  }
}
