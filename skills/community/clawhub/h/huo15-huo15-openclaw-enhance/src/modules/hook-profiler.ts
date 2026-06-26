/**
 * 模块: hook-profiler（v5.8.0）
 *
 * 量化 OpenClaw 端到端首字延迟。三路数据汇合到 enhance-memory.sqlite：
 *   1. log-tailer 解析 ~/.openclaw/logs/gateway.err.log
 *      - [trace:embedded-run] prep stages: ...        → prep_stage_metrics
 *      - [hooks] X handler from <plugin> failed: timed out → hook_profile (timeout)
 *      - [hooks] X handler from <plugin> threw: ...   → hook_profile (error)
 *   2. profileHook wrapper（src/utils/profile-hook.ts）— enhance 自家 hook 精确测时
 *   3. （未来）若 openclaw 暴露其它 plugin 的成功 handler 事件可补
 *
 * 工具 enhance_hook_doctor 给出近 N 天 P50/P95/timeout 排行 + 行动建议（return-cliCmd
 * 模式，不替用户改 openclaw.json，红线 #5）。
 *
 * 设计约束：
 *  - 不用 child_process（红线 #4）— 用 fs.watch + readSync 增量读
 *  - 启动时跳到日志末尾，只解析"启动后新增"的内容
 *  - 写表失败一律静默；profiler 不能影响主流程
 */
import {
  closeSync,
  existsSync,
  openSync,
  readSync,
  statSync,
  watch as fsWatch,
  type FSWatcher,
} from "node:fs";
import { join } from "node:path";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { getDb } from "../utils/sqlite-store.js";
import {
  insertHookProfile,
  insertPrepStage,
  purgeOldHookProfiles,
  getPrepStageStats,
  getHookProfileStats,
  listKnownHookEvents,
} from "../utils/hook-profile-db.js";
import type { HookProfilerConfig } from "../types.js";

// ─────────────────────── log-tailer ───────────────────────

const PREP_STAGE_RE =
  /\[trace:embedded-run\]\s+prep\s+stages:\s+runId=(\S+)\s+sessionId=(\S+)\s+phase=stream-ready\s+totalMs=(\d+)\s+stages=(.+)/;
const HOOK_TIMEOUT_RE =
  /\[hooks\]\s+(\w+)\s+handler\s+from\s+(\S+)\s+failed:\s+timed\s+out\s+after\s+(\d+)ms/;
const HOOK_ERROR_RE =
  /\[hooks\]\s+(\w+)\s+handler\s+from\s+(\S+)\s+threw:\s+(.+)/;
const TS_RE =
  /^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:\d{2})?)\s+/;

function parseTimestamp(line: string): number {
  const m = line.match(TS_RE);
  if (m) {
    const t = Date.parse(m[1]);
    if (!Number.isNaN(t)) return t;
  }
  return Date.now();
}

function parseStageMap(stagesStr: string): Record<string, number> {
  // "workspace-sandbox:0ms@0ms,skills:0ms@0ms,core-plugin-tools:5252ms@5252ms,..."
  const out: Record<string, number> = {};
  for (const seg of stagesStr.split(",")) {
    const m = seg.match(/^(\S+?):(\d+)ms@/);
    if (m) out[m[1]] = parseInt(m[2], 10);
  }
  return out;
}

function processLine(line: string): void {
  if (line.length === 0) return;
  const ts = parseTimestamp(line);

  let m = line.match(PREP_STAGE_RE);
  if (m) {
    const [, runId, sessionId, totalMsStr, stagesStr] = m;
    const stages = parseStageMap(stagesStr);
    try {
      insertPrepStage(getDb(), {
        ts,
        run_id: runId,
        session_id: sessionId,
        total_ms: parseInt(totalMsStr, 10),
        workspace_sandbox_ms: stages["workspace-sandbox"] ?? -1,
        skills_ms: stages["skills"] ?? -1,
        core_plugin_tools_ms: stages["core-plugin-tools"] ?? -1,
        bootstrap_context_ms: stages["bootstrap-context"] ?? -1,
        bundle_tools_ms: stages["bundle-tools"] ?? -1,
        system_prompt_ms: stages["system-prompt"] ?? -1,
        session_resource_loader_ms: stages["session-resource-loader"] ?? -1,
        agent_session_ms: stages["agent-session"] ?? -1,
        stream_setup_ms: stages["stream-setup"] ?? -1,
        raw_line: line.slice(0, 4000),
      });
    } catch {
      // 静默
    }
    return;
  }

  m = line.match(HOOK_TIMEOUT_RE);
  if (m) {
    const [, hookEvent, pluginId, durationStr] = m;
    try {
      insertHookProfile(getDb(), {
        ts,
        source: "log-timeout",
        hook_event: hookEvent,
        plugin_id: pluginId,
        module: null,
        duration_ms: parseInt(durationStr, 10),
        status: "timeout",
        err_msg: `timed out after ${durationStr}ms`,
      });
    } catch {
      // 静默
    }
    return;
  }

  m = line.match(HOOK_ERROR_RE);
  if (m) {
    const [, hookEvent, pluginId, errMsg] = m;
    try {
      insertHookProfile(getDb(), {
        ts,
        source: "log-error",
        hook_event: hookEvent,
        plugin_id: pluginId,
        module: null,
        duration_ms: null,
        status: "error",
        err_msg: errMsg.slice(0, 500),
      });
    } catch {
      // 静默
    }
    return;
  }
}

interface TailerState {
  watcher: FSWatcher | null;
  lastOffset: number;
  buffer: string;
  filePath: string | null;
}
const tailer: TailerState = {
  watcher: null,
  lastOffset: 0,
  buffer: "",
  filePath: null,
};

const MAX_CHUNK_BYTES = 1024 * 1024; // 单次最多读 1MB，防大批量历史日志一次性灌爆 DB

function readNew(): void {
  if (!tailer.filePath) return;
  let st;
  try {
    st = statSync(tailer.filePath);
  } catch {
    return;
  }
  if (st.size < tailer.lastOffset) {
    // 日志被轮转/截断，重置
    tailer.lastOffset = 0;
    tailer.buffer = "";
  }
  if (st.size === tailer.lastOffset) return;

  const fd = openSync(tailer.filePath, "r");
  try {
    const len = st.size - tailer.lastOffset;
    const buf = Buffer.alloc(Math.min(len, MAX_CHUNK_BYTES));
    const bytesRead = readSync(fd, buf, 0, buf.length, tailer.lastOffset);
    tailer.lastOffset += bytesRead;
    const text = tailer.buffer + buf.slice(0, bytesRead).toString("utf8");
    const lines = text.split(/\r?\n/);
    tailer.buffer = lines.pop() ?? "";
    for (const line of lines) processLine(line);
  } finally {
    closeSync(fd);
  }
}

function startLogTailer(api: OpenClawPluginApi, openclawHome: string): void {
  const filePath = join(openclawHome, "logs", "gateway.err.log");
  if (!existsSync(filePath)) {
    api.logger.info(
      `[enhance-hook-profiler] gateway.err.log 不存在，log-tailer 暂不启动（首次启动 openclaw 后会出现）`,
    );
    return;
  }
  tailer.filePath = filePath;
  // 启动时跳到末尾，只解析"启动后新增"的日志（避免冷启动一次性灌入 N 个月历史）
  try {
    tailer.lastOffset = statSync(filePath).size;
  } catch {
    tailer.lastOffset = 0;
  }
  tailer.buffer = "";

  try {
    tailer.watcher = fsWatch(filePath, { persistent: false }, (eventType) => {
      if (eventType === "change") readNew();
    });
    api.logger.info(
      `[enhance-hook-profiler] log-tailer 已启动 (offset=${tailer.lastOffset}, path=${filePath})`,
    );
  } catch (err) {
    api.logger.warn(
      `[enhance-hook-profiler] log-tailer 启动失败: ${err instanceof Error ? err.message : String(err)}`,
    );
  }
}

function stopLogTailer(): void {
  if (tailer.watcher) {
    try {
      tailer.watcher.close();
    } catch {
      // ignore
    }
    tailer.watcher = null;
  }
}

// ─────────────────────── enhance_hook_doctor 工具 ───────────────────────

function fmtMs(ms: number): string {
  if (ms < 0) return "n/a";
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

function pad(s: string, n: number): string {
  if (s.length >= n) return s;
  return s + " ".repeat(n - s.length);
}

function registerHookDoctorTool(api: OpenClawPluginApi): void {
  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_hook_doctor",
      description:
        "诊断 OpenClaw 首字延迟：基于近 N 天 prep-stages + hook profile 数据，分析 system-prompt / core-plugin-tools 等阶段慢点和各 plugin hook 排行。不修改 openclaw.json，给 cli 命令让用户决定（return-cliCmd 模式）。",
      parameters: Type.Object({
        days: Type.Optional(
          Type.Number({ description: "回溯多少天，默认 7", default: 7 }),
        ),
        topK: Type.Optional(
          Type.Number({
            description: "每个 hook event 显示前 K 名 plugin，默认 10",
            default: 10,
          }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const days = (params.days as number) ?? 7;
        const topK = (params.topK as number) ?? 10;
        const sinceMs = Date.now() - days * 86400_000;
        const db = getDb();

        const prep = getPrepStageStats(db, sinceMs);
        const events = listKnownHookEvents(db, sinceMs);

        const lines: string[] = [];
        lines.push(
          `=== prep-stages 趋势（近 ${days} 天，${prep.count} 条样本）===`,
        );
        if (prep.count === 0) {
          lines.push(
            "（暂无数据。log-tailer 从启动后增量抓取 gateway.err.log，运行几次 turn 后再来看。）",
          );
        } else {
          lines.push(
            `total_ms       p50=${fmtMs(prep.total_ms.p50)}  p95=${fmtMs(prep.total_ms.p95)}  max=${fmtMs(prep.total_ms.max)}`,
          );
          lines.push(
            `core_plugin    p50=${fmtMs(prep.core_plugin_tools_ms.p50)}  p95=${fmtMs(prep.core_plugin_tools_ms.p95)}`,
          );
          lines.push(
            `system_prompt  p50=${fmtMs(prep.system_prompt_ms.p50)}  p95=${fmtMs(prep.system_prompt_ms.p95)}`,
          );
          lines.push(
            `bundle_tools   p50=${fmtMs(prep.bundle_tools_ms.p50)}  p95=${fmtMs(prep.bundle_tools_ms.p95)}`,
          );
          lines.push(
            `session_loader p50=${fmtMs(prep.session_resource_loader_ms.p50)}  p95=${fmtMs(prep.session_resource_loader_ms.p95)}`,
          );
          lines.push(
            `bootstrap_ctx  p50=${fmtMs(prep.bootstrap_context_ms.p50)}  p95=${fmtMs(prep.bootstrap_context_ms.p95)}`,
          );
          lines.push(
            `stream_setup   p50=${fmtMs(prep.stream_setup_ms.p50)}  p95=${fmtMs(prep.stream_setup_ms.p95)}  ← 模型端，本地不可干预`,
          );
        }

        if (events.length === 0) {
          lines.push("");
          lines.push("=== hook 排行 ===");
          lines.push(
            "（暂无 hook profile 数据。log-tailer 仅在出现 timeout/error 时记录其它 plugin 的事件；enhance 内部模块需用 profileHook 包装才会写成功耗时。）",
          );
        }

        for (const ev of events) {
          const stats = getHookProfileStats(db, ev, sinceMs).slice(0, topK);
          if (stats.length === 0) continue;
          lines.push("");
          lines.push(
            `=== ${ev} hook 排行（按 p95 降序，前 ${stats.length}）===`,
          );
          lines.push(
            pad("plugin", 38) +
              pad("module", 22) +
              pad("count", 8) +
              pad("p50", 10) +
              pad("p95", 10) +
              "异常",
          );
          for (const s of stats) {
            const mod = s.module ?? "(unknown)";
            const flag =
              s.timeout_count > 0
                ? `${s.timeout_count}t/${s.error_count}e`
                : s.error_count > 0
                  ? `${s.error_count}e`
                  : "";
            lines.push(
              pad(s.plugin_id.slice(0, 36), 38) +
                pad(mod.slice(0, 20), 22) +
                pad(String(s.count), 8) +
                pad(fmtMs(s.p50), 10) +
                pad(fmtMs(s.p95), 10) +
                flag,
            );
          }
        }

        // ── 行动建议（不替用户改配置，只给信号）──
        lines.push("");
        lines.push("=== 行动建议 ===");
        const advice: string[] = [];
        if (prep.count > 0) {
          if (prep.system_prompt_ms.p95 > 3000) {
            advice.push(
              `• system_prompt p95=${fmtMs(prep.system_prompt_ms.p95)} 偏高 → 看上面 before_prompt_build 排行定位是哪个 plugin 拖慢`,
            );
          }
          if (prep.core_plugin_tools_ms.p50 > 4000) {
            advice.push(
              `• core_plugin_tools p50=${fmtMs(prep.core_plugin_tools_ms.p50)} 偏高 → 跑 enhance_config_doctor 看是否有 plugin-legacy-tool-fields warning（malformed tool 浪费 SDK 验证时间）`,
            );
          }
          if (prep.bundle_tools_ms.p95 > 2000) {
            advice.push(
              `• bundle_tools p95=${fmtMs(prep.bundle_tools_ms.p95)} 高方差 → tool schema 总量过大，考虑把 enhance toolTier 调成 balanced/minimal`,
            );
          }
        }
        const seenTimeoutPairs = new Set<string>();
        for (const ev of events) {
          for (const s of getHookProfileStats(db, ev, sinceMs)) {
            if (
              s.timeout_count > 0 &&
              s.plugin_id !== "@huo15/openclaw-enhance"
            ) {
              const key = `${s.plugin_id}::${ev}`;
              if (seenTimeoutPairs.has(key)) continue;
              seenTimeoutPairs.add(key);
              advice.push(
                `• ${s.plugin_id} 在 ${ev} 上发生过 ${s.timeout_count} 次 timeout → 反馈给该 plugin 维护方，或检查其连接/重试策略`,
              );
            }
          }
        }
        if (advice.length === 0) {
          lines.push("（未检测到明显异常）");
        } else {
          for (const a of advice) lines.push(a);
        }

        lines.push("");
        lines.push(`参数：days=${days} topK=${topK}（调高 days 看长期趋势）`);

        return {
          content: [{ type: "text" as const, text: lines.join("\n") }],
        };
      },
    })) as any,
    { name: "enhance_hook_doctor" },
  );
}

// ─────────────────────── 主入口 ───────────────────────

export function registerHookProfiler(
  api: OpenClawPluginApi,
  openclawHome: string,
  config?: HookProfilerConfig,
): void {
  const enabled = config?.enabled !== false;
  if (!enabled) {
    api.logger.info(
      `[enhance-hook-profiler] 已禁用（config.hookProfiler.enabled=false）`,
    );
    return;
  }

  // 启动期清理 30 天前的旧数据
  try {
    const r = purgeOldHookProfiles(getDb(), config?.retentionDays ?? 30);
    if (r.deleted > 0) {
      api.logger.info(
        `[enhance-hook-profiler] 清理 ${r.deleted} 条 ${config?.retentionDays ?? 30} 天前旧数据`,
      );
    }
  } catch {
    // 静默
  }

  // 启动 log-tailer（若 logs/gateway.err.log 存在）
  if (config?.tailer?.enabled !== false) {
    startLogTailer(api, openclawHome);
  }

  // 注册 enhance_hook_doctor 工具
  registerHookDoctorTool(api);

  api.logger.info(
    `[enhance] hook-profiler 模块已加载（log-tailer + enhance_hook_doctor 工具；非侵入诊断 OpenClaw 首字延迟）`,
  );
}

export { stopLogTailer };
