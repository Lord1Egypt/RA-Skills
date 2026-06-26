/**
 * v5.7.16 trajectory 体量诊断模块
 *
 * 启动期 + 工具按需，扫描 ~/.openclaw/agents/*\/sessions/*.trajectory.jsonl，
 * 发现单文件 ≥ 阈值 或 累计 ≥ 阈值 时 warn 并给归档 cliCmd。
 *
 * 触发场景：openclaw-control-ui webchat 反复 sessions.list，gateway 主线程
 * 在 V8 JsonParser::ParseJsonObject 上被超大 trajectory 钉死，95%+ CPU。
 * 单次 sessions.list 实测 12-14s，最长观测到 367s（event-loop max delay 13s+）。
 *
 * 红线（CLAUDE.md §11.4 / §6.4 一致）：
 * - 完全只读 trajectory 文件（仅 readdir+stat，不 readFile）—— 自己也不能踩 JSON.parse 大文件
 * - 不删/不改/不归档 trajectory，归档命令通过 return-cliCmd 模式给出（红线 #5）
 * - 不调用 openclaw 任何 sessions/* API（红线 #2 不复制龙虾原生功能）
 * - 不用 child_process（红线 #4）
 */
import { readdirSync, statSync, existsSync } from "node:fs";
import { join } from "node:path";
import { Type } from "@sinclair/typebox";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import type { SessionDoctorConfig, NotificationQueue } from "../types.js";
import { DEFAULT_AGENT_ID } from "../types.js";

interface CheckResult {
  ok: boolean;
  level: "info" | "warn" | "error";
  category: string;
  message: string;
  fixCommand?: string;
}

interface TrajectoryFile {
  path: string;
  agent: string;
  sessionId: string;
  sizeBytes: number;
  sizeMB: number;
  mtimeMs: number;
  mtimeDaysAgo: number;
}

const MB = 1024 * 1024;

/**
 * 只读扫 ~/.openclaw/agents/<agent>/sessions/*.trajectory.jsonl
 * 仅取文件大小 + mtime，不读内容（避免自己也踩 JSON.parse 大文件的坑）
 */
export function scanTrajectories(openclawDir: string): TrajectoryFile[] {
  const out: TrajectoryFile[] = [];
  const agentsDir = join(openclawDir, "agents");
  if (!existsSync(agentsDir)) return out;

  const now = Date.now();
  let agents: string[];
  try {
    agents = readdirSync(agentsDir);
  } catch {
    return out;
  }

  for (const agent of agents) {
    const sessionsDir = join(agentsDir, agent, "sessions");
    if (!existsSync(sessionsDir)) continue;

    let entries: string[];
    try {
      entries = readdirSync(sessionsDir);
    } catch {
      continue;
    }

    for (const f of entries) {
      if (!f.endsWith(".trajectory.jsonl")) continue;
      const p = join(sessionsDir, f);
      try {
        const st = statSync(p);
        if (!st.isFile()) continue;
        out.push({
          path: p,
          agent,
          sessionId: f.replace(/\.trajectory\.jsonl$/, ""),
          sizeBytes: st.size,
          sizeMB: st.size / MB,
          mtimeMs: st.mtimeMs,
          mtimeDaysAgo: (now - st.mtimeMs) / 86400000,
        });
      } catch {
        /* skip 单个文件读不到也不影响 */
      }
    }
  }
  return out;
}

export function checkTrajectories(
  openclawDir: string,
  options: SessionDoctorConfig = {},
): CheckResult[] {
  const warnSingle = options.warnSingleFileMB ?? 20;
  const warnTotal = options.warnTotalMB ?? 200;
  const archiveDays = options.archiveAgeDays ?? 7;
  const topN = options.topN ?? 5;

  const files = scanTrajectories(openclawDir);
  if (files.length === 0) {
    return [
      {
        ok: true,
        level: "info",
        category: "trajectory-empty",
        message: "未发现 trajectory.jsonl 文件",
      },
    ];
  }

  const totalMB = files.reduce((s, f) => s + f.sizeMB, 0);
  const huge = files
    .filter((f) => f.sizeMB >= warnSingle)
    .sort((a, b) => b.sizeMB - a.sizeMB);
  // v6.1.0 路径策略：归档目录从 sessions/.archive 提升到 sessions-archive
  // (跟 sessions/ 平级，不在子树) → openclaw sessions.list 不会扫到。
  // 5/2 sample 实证 v1 路径策略不解决卡顿（99.2% 主线程仍卡 JsonParser）。
  const archiveDir = join(openclawDir, "agents", "main", "sessions-archive");

  const results: CheckResult[] = [];

  // 1. 累计体量超阈值 → 给批量归档命令
  //    批量命令限制条件：size > warnSingle 且 mtime > archiveDays 天前
  //    （活动中的 session 不会被误归档）
  if (totalMB >= warnTotal) {
    results.push({
      ok: false,
      level: "warn",
      category: "trajectory-total-huge",
      message:
        `trajectory.jsonl 累计 ${totalMB.toFixed(0)}MB（${files.length} 个文件，阈值 ${warnTotal}MB）。` +
        `gateway 的 sessions.list 会在主线程 JSON.parse 这些文件，超大时卡 event-loop（曾观测到单次 12-14s，最长 367s，event-loop max delay 13s+，95%+ CPU；5/2 sample 实测 99.2% 主线程卡 V8 JsonParser）。` +
        `v6.1.0 起归档目标改为 sessions-archive（移出 sessions/ 子树，openclaw 不再扫）。建议跑 enhance_trajectory_archiver_setup 部署 LaunchAgent 自动归档。`,
      fixCommand:
        `# 一次性手动归档（主推 enhance_trajectory_archiver_setup 部署自动版）：\n` +
        `mkdir -p '${archiveDir}' && find '${join(openclawDir, "agents")}' -name '*.trajectory.jsonl' -size +${warnSingle}M -mtime +${archiveDays} -exec mv {} '${archiveDir}/' \\;`,
    });
  }

  // 2. 单文件超大 → 列出 top N 路径，让用户挨个判断
  //    不给批量 cliCmd（避免归档活动中的大 session）
  if (huge.length > 0) {
    const top = huge.slice(0, topN);
    const lines = top
      .map(
        (f) =>
          `  - ${f.sizeMB.toFixed(1)}MB  ${f.mtimeDaysAgo.toFixed(0)}d ago  ${f.path}`,
      )
      .join("\n");
    const more = huge.length > topN ? `\n  ... 共 ${huge.length} 个 ≥ ${warnSingle}MB` : "";
    results.push({
      ok: false,
      level: "warn",
      category: "trajectory-single-huge",
      message:
        `检测到 ${huge.length} 个 trajectory.jsonl 单文件 ≥ ${warnSingle}MB（top ${Math.min(topN, huge.length)}）:\n${lines}${more}`,
      fixCommand:
        `# 请逐个检查后归档（确认 session 不再活跃），目标是 sessions-archive（v6.1.0 路径，移出 sessions/ 子树）：\n` +
        `mkdir -p '${archiveDir}'\n` +
        `# mv '<path>' '${archiveDir}/'`,
    });
  }

  if (results.length === 0) {
    return [
      {
        ok: true,
        level: "info",
        category: "trajectory-ok",
        message: `trajectory 体量健康（${files.length} 个文件，累计 ${totalMB.toFixed(0)}MB）`,
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
      if (r.fixCommand) line += `\n   → 修复:\n${r.fixCommand}`;
      return line;
    })
    .join("\n\n");
}

export function registerSessionDoctor(
  api: OpenClawPluginApi,
  config: SessionDoctorConfig | undefined,
  notifyQueue: NotificationQueue | null,
) {
  const openclawDir = resolveOpenClawHome(api);

  // 启动期检查（fire-and-forget，绝不阻塞插件加载）
  // 本模块不读 db，notifyQueue 缺失时降级到 logger only（符合 enhance "无状态模块
  // 在 DB 降级模式仍正常加载" 原则）。
  try {
    const results = checkTrajectories(openclawDir, config);
    const issues = results.filter((r) => !r.ok);
    if (issues.length > 0) {
      api.logger.warn(
        `[enhance-session-doctor] 检测到 ${issues.length} 项 trajectory 体量问题:`,
      );
      for (const r of issues) {
        api.logger.warn(`  • [${r.level}] ${r.category}: ${r.message}`);
        if (r.fixCommand) api.logger.warn(`    → ${r.fixCommand}`);
      }
      if (notifyQueue) {
        notifyQueue.emit(
          DEFAULT_AGENT_ID,
          "warn",
          "session-doctor",
          `enhance: trajectory.jsonl 体量异常（${issues.length} 项），可能引起 gateway sessions.list 卡顿`,
          formatResults(issues) + "\n\n（运行 enhance_session_doctor 工具看完整诊断）",
        );
      }
    } else {
      api.logger.info("[enhance-session-doctor] trajectory 体量健康");
    }
  } catch (err) {
    api.logger.error(
      `[enhance-session-doctor] 启动检查失败（不影响插件其它功能）: ${(err as Error).message}`,
    );
  }

  // 工具：手动触发完整诊断（输出可粘贴的归档命令）
  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_session_doctor",
      description:
        "诊断 ~/.openclaw/agents/*/sessions/*.trajectory.jsonl 体量是否会卡 gateway 主线程。" +
        "症状：gateway 99% CPU 持续不退、sessions.list 单次 12s+、event-loop max delay 10s+。" +
        "只读，给归档 cliCmd 不自动执行。",
      parameters: Type.Object({}),
      async execute() {
        const results = checkTrajectories(openclawDir, config);
        const text = formatResults(results);
        return { content: [{ type: "text" as const, text }] };
      },
    })) as any,
    { name: "enhance_session_doctor" },
  );

  api.logger.info(
    "[enhance] trajectory 体量诊断模块已加载（只读，不删/不归档 trajectory）",
  );
}
