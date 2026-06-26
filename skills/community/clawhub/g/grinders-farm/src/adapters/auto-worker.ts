/**
 * Background worker: advances one in-game day every `intervalSec` seconds.
 * Writes ~/.grinders-farm/auto.pid and auto.config.json.
 */
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { GameEngine } from "../game/engine.js";
import { LocalStorage } from "../storage/local-storage.js";
import { loadNotifyConfig, pushFarmSnapshot, shouldNotifyOnAutoAdvance } from "../notify/openclaw-push.js";

const DATA_DIR = path.join(os.homedir(), ".grinders-farm");
const PID_FILE = path.join(DATA_DIR, "auto.pid");
const CONFIG_FILE = path.join(DATA_DIR, "auto.config.json");
const LOG_FILE = path.join(DATA_DIR, "auto.log");

const intervalSec = Math.max(1, parseInt(process.argv[2] ?? "3600", 10));

fs.mkdirSync(DATA_DIR, { recursive: true });
fs.writeFileSync(PID_FILE, String(process.pid), "utf8");
fs.writeFileSync(
  CONFIG_FILE,
  JSON.stringify({ intervalSec, startedAt: new Date().toISOString(), pid: process.pid }, null, 2),
  "utf8",
);

function log(line: string): void {
  const entry = `[${new Date().toISOString()}] ${line}\n`;
  try {
    fs.appendFileSync(LOG_FILE, entry, "utf8");
  } catch {
    /* ignore */
  }
}

function cleanup(): void {
  try {
    fs.unlinkSync(PID_FILE);
  } catch {
    /* ignore */
  }
  try {
    fs.unlinkSync(CONFIG_FILE);
  } catch {
    /* ignore */
  }
  process.exit(0);
}

process.on("SIGINT", cleanup);
process.on("SIGTERM", cleanup);

log(`started pid=${process.pid} intervalSec=${intervalSec}`);

async function tick(): Promise<void> {
  // Recreate engine each tick so manual commands (plant/water/harvest) written by
  // other processes are picked up from ~/.grinders-farm/farm.json.
  const storage = new LocalStorage();
  const engine = new GameEngine(storage);
  const result = await engine.advanceDay();
  log(result.success ? "auto advance ok" : `auto advance fail: ${result.message.slice(0, 200)}`);

  if (!result.success) return;

  if (!shouldNotifyOnAutoAdvance()) {
    const cfg = loadNotifyConfig();
    if (!cfg) {
      log("notify skipped: no delivery config。在聊天发 /farm 或设 GRINDERS_FARM_NOTIFY_TARGET（见 SKILL）。");
    } else if (cfg.onAutoAdvance === false) {
      log("notify skipped: onAutoAdvance 已关闭（notify.json 或环境变量）");
    } else {
      log("notify skipped");
    }
    return;
  }

  try {
    const push = await pushFarmSnapshot();
    log(push.ok ? "notify ok" : `notify skip/fail: ${push.message.slice(0, 300)}`);
  } catch (err) {
    log(`notify error: ${err instanceof Error ? err.message : String(err)}`);
  }
}

setInterval(() => {
  tick().catch((err) => log(`tick error: ${err instanceof Error ? err.message : String(err)}`));
}, intervalSec * 1000);
