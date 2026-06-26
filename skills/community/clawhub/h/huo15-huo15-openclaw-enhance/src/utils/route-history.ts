/**
 * v5.8.6 模型路由历史快照
 *
 * 每次 latency-tracker flushTracking 同步追加一行 JSONL 到
 * ~/.openclaw/enhance/model-route-history.jsonl，保留最近 N 条（环形）。
 * 用于回看趋势：sidus 是不是在从 429 恢复 / deepseek 高峰是否变慢。
 *
 * 红线：
 *   - 复用 latency-tracker 的 flush 节流（不增新 timer）
 *   - 损坏时 silent fallback（不阻塞 hook 流程）
 *   - JSONL append-only 写入 + 周期性 truncate（保留最近 N 条）
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync, renameSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import type { SpeedSample } from "./model-route-config.js";

export interface HistorySnapshot {
  /** ISO 时间戳 */
  ts: string;
  /** providerId → 当时的 P50/P95/errRate/samples */
  providers: Record<string, SpeedSample>;
}

const MAX_RETAINED = 288;  // 默认 24h × 12 (每 5 分钟一次) ≈ 288 条；> 阈值时 trim
const TRIM_WHEN_OVER = 320;

export function getHistoryPath(): string {
  return join(homedir(), ".openclaw", "enhance", "model-route-history.jsonl");
}

export function appendSnapshot(snap: HistorySnapshot): void {
  const p = getHistoryPath();
  const dir = dirname(p);
  if (!existsSync(dir)) {
    try {
      mkdirSync(dir, { recursive: true });
    } catch {
      return;
    }
  }
  try {
    appendFileSync(p, JSON.stringify(snap) + "\n", "utf-8");
  } catch {
    // 写盘失败不阻塞 hook 流
    return;
  }
  // 每写 ~50 次抽样 trim 一次（避免每次都读全文件）
  if (Math.random() < 0.02) trimIfNeeded();
}

export function readHistory(opts?: {
  /** 只保留最近 N 小时；默认 24 */
  windowHours?: number;
  /** 仅返回某个 providerId（substring 匹配） */
  providerFilter?: string;
}): HistorySnapshot[] {
  const p = getHistoryPath();
  if (!existsSync(p)) return [];
  let raw: string;
  try {
    raw = readFileSync(p, "utf-8");
  } catch {
    return [];
  }
  const lines = raw.split(/\r?\n/).filter(Boolean);
  const out: HistorySnapshot[] = [];
  const cutoffMs = opts?.windowHours
    ? Date.now() - opts.windowHours * 3600_000
    : 0;
  const filter = opts?.providerFilter ?? "";
  for (const ln of lines) {
    try {
      const snap = JSON.parse(ln) as HistorySnapshot;
      if (cutoffMs && Date.parse(snap.ts) < cutoffMs) continue;
      if (filter) {
        // 只保留含某 provider 的快照（providers 字段过滤后非空）
        const filtered: Record<string, SpeedSample> = {};
        for (const [k, v] of Object.entries(snap.providers || {})) {
          if (k.includes(filter)) filtered[k] = v;
        }
        if (Object.keys(filtered).length === 0) continue;
        snap.providers = filtered;
      }
      out.push(snap);
    } catch {
      /* skip 损坏行 */
    }
  }
  return out;
}

/**
 * 砍最旧 N 条到 MAX_RETAINED。复用 atomic write（tmp + rename）。
 */
export function trimIfNeeded(): void {
  const p = getHistoryPath();
  if (!existsSync(p)) return;
  let raw: string;
  try {
    raw = readFileSync(p, "utf-8");
  } catch {
    return;
  }
  const lines = raw.split(/\r?\n/).filter(Boolean);
  if (lines.length <= TRIM_WHEN_OVER) return;
  const kept = lines.slice(-MAX_RETAINED).join("\n") + "\n";
  const tmp = `${p}.tmp`;
  try {
    writeFileSync(tmp, kept, "utf-8");
    renameSync(tmp, p);
  } catch {
    /* 写失败下次再试 */
  }
}

/**
 * 把一组数值渲染成 ASCII spark line（用 ▁▂▃▄▅▆▇█ 8 级）。
 */
export function sparkLine(values: number[]): string {
  if (values.length === 0) return "";
  const blocks = "▁▂▃▄▅▆▇█";
  const min = Math.min(...values);
  const max = Math.max(...values);
  if (max === min) return blocks[0].repeat(values.length);
  const range = max - min;
  return values
    .map((v) => {
      const idx = Math.min(7, Math.floor(((v - min) / range) * 8));
      return blocks[idx];
    })
    .join("");
}
