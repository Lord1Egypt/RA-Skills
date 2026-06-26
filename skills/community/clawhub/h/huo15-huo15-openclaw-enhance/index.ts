/**
 * 龙虾增强包 (OpenClaw Enhancement Kit)
 *
 * 非侵入式增强插件（v1.2.3 — 多 Agent 隔离）：
 * - 模块1: 结构化记忆系统（按 agentId 隔离，借鉴 Claude Code auto-memory）
 * - 模块2: 工具安全守卫（按 agentId 记录日志，借鉴 Claude Code 权限系统）
 * - 模块3: 提示词增强（按 agentId 注入上下文，借鉴 Claude Code systemPromptSections）
 * - 模块4: 工作流自动化（按 agentId 隔离工作流，借鉴 Claude Code hooks 事件驱动）
 * - 模块5: 增强仪表盘（支持按 Agent 筛选）
 *
 * 完全适配 WeCom 插件的动态 Agent 功能：
 * - 工具使用 OpenClawPluginToolFactory 模式，从 ctx.agentId 获取当前 Agent
 * - 钩子从 ctx.agentId 获取当前 Agent
 * - 每个企微用户/群组的数据完全隔离
 */
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { wrapApiForSafeHooks } from "./src/utils/safe-api-wrapper.js";
import { createRequire } from "node:module";
const pkg = createRequire(import.meta.url)("../package.json") as { version: string };
import { registerStructuredMemory } from "./src/modules/structured-memory.js";
import { registerTaskPlanner } from "./src/modules/task-planner.js";
import { registerToolSafety } from "./src/modules/tool-safety.js";
import { registerPromptEnhancer } from "./src/modules/prompt-enhancer.js";
import { registerWorkflowHooks } from "./src/modules/workflow-hooks.js";
import { registerDashboard } from "./src/modules/dashboard.js";

import { registerSelfCheck } from "./src/modules/self-check.js";
import { registerMemoryIntegrator } from "./src/modules/memory-integrator.js";
import { registerTodoTracker } from "./src/modules/todo-tracker.js";
import { registerChapterMarks } from "./src/modules/chapter-marks.js";
import { registerModeGate } from "./src/modules/mode-gate.js";
import { registerStatusline } from "./src/modules/statusline.js";
import { registerSpawnTask } from "./src/modules/spawn-task.js";
import { registerSkillDoctor } from "./src/modules/skill-doctor.js";
import { registerScheduledTasksBridge } from "./src/modules/scheduled-tasks-bridge.js";
import { registerSkillInstaller, CLAW_HUB_SKILLS } from "./src/modules/skill-installer.js";
import { registerKbCorpus } from "./src/modules/kb-corpus.js";
import { registerSessionRecap } from "./src/modules/session-recap.js";
import { registerTranscriptSearch } from "./src/modules/transcript-search.js";
import { registerConfigDoctor } from "./src/modules/config-doctor.js";
import { registerSessionDoctor } from "./src/modules/session-doctor.js";
import { registerTrajectoryArchiver } from "./src/modules/trajectory-archiver.js";
import { registerSkillRecommender } from "./src/modules/skill-recommender.js";
import { registerSessionLifecycle } from "./src/modules/session-lifecycle.js";
import { registerNativeMemorySurfacer } from "./src/modules/native-memory-surfacer.js";
import { registerBotShareLink } from "./src/modules/bot-share-link.js";
import { registerBotUploadLink } from "./src/modules/bot-upload-link.js";
import { registerContextWatchdog } from "./src/modules/context-watchdog.js";
import { registerSessionBridge } from "./src/modules/session-bridge.js";
import { registerHookProfiler } from "./src/modules/hook-profiler.js";
import { registerCcBridgePrompt } from "./src/modules/cc-bridge-prompt.js";
import { registerCcBridgePreFetch } from "./src/modules/cc-bridge-pre-fetch.js";
import { registerCcBridgeDispatchHarness } from "./src/modules/cc-bridge-dispatch-harness.js";
import { registerCcBridgeKeywordDispatch } from "./src/modules/cc-bridge-keyword-dispatch.js";
import { registerModelRouter } from "./src/modules/model-router.js";
import { registerLargeFileBridge } from "./src/modules/large-file-bridge.js";
import { createNotificationQueue } from "./src/modules/notification-queue.js";
import { resolveOpenClawHome } from "./src/utils/resolve-home.js";
import { initDb } from "./src/utils/sqlite-store.js";
import type { EnhancePluginConfig, ToolTier } from "./src/types.js";
import { existsSync } from "node:fs";
import { join } from "node:path";

/**
 * 工具分层映射（v5.6）：
 * - L1 minimal: 记忆核心 / 状态栏 / spawn / 模式 / 章节 / installer / integrator
 * - L2 balanced (default): +todo / 定时任务桥
 * - L3 full: +workflow / safety / task-planner / session-recap / skill-doctor
 *
 * 只会载入 tier 内的模块，其他模块整个不 register（省下 tool schema 全部重量）。
 */
type Tier = 1 | 2 | 3;
const TIER_MAX: Record<ToolTier, Tier> = {
  minimal: 1,
  balanced: 2,
  full: 3,
};

export default definePluginEntry({
  id: "enhance",
  name: "龙虾增强包 (OpenClaw Enhancement Kit)",
  description: "结构化记忆、工具安全守卫、提示词增强、工作流自动化、仪表盘",

  register(rawApi) {
    // v6.6.8: 全模块 hook 防御性包裹 — 拦截 api.on()，让所有 enhance 模块（28 hook 跨 17 文件）
    // 的 hook handler 自动包 try/catch。任何 hook 抛 → log + return undefined，不影响 OpenClaw 主流程。
    // 修用户 v6.6.5-v6.6.7 升级后仍反复撞 "Something went wrong" 事故（根因不在 ctx-watchdog，
    // 而在其他模块未受保护的 hook）。
    const api = wrapApiForSafeHooks(rawApi);

    const config = (api.pluginConfig ?? {}) as EnhancePluginConfig;
    const toolTier: ToolTier = config.toolTier ?? "balanced";
    const maxTier: Tier = TIER_MAX[toolTier];

    // 初始化共享数据库和通知队列
    // better-sqlite3 是原生模块，Node.js 版本变更时 ABI 不兼容导致加载失败。
    // v5.7.17: 走 createRequire(import.meta.url) 同步加载（loader 拒绝
    // async register —— 见 ~/.claude/projects/-Users-jobzhao/memory/feedback_*
    // 关于 openclaw plugin SDK sync 约束的记录），try/catch 仍可截获 ABI 错误。
    // .node-version 指纹文件用于提前检测 Node 升级，在加载前就打 warning。
    const openclawHome = resolveOpenClawHome(api);
    const extDir = join(openclawHome, "extensions", "enhance");
    let db: ReturnType<typeof initDb> | null = null;
    let notifyQueue: ReturnType<typeof createNotificationQueue> | null = null;
    let dbAvailable = false;
    try {
      db = initDb(openclawHome, extDir, api.logger);
      notifyQueue = createNotificationQueue(db, config.notifications);
      dbAvailable = true;
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      api.logger.error(
        `[enhance] better-sqlite3 原生绑定丢失，数据库初始化失败：${msg}`,
      );
      api.logger.error(
        `[enhance] 修复命令：cd ${extDir} && npm rebuild better-sqlite3`,
      );
      api.logger.warn(
        `[enhance] 已降级：跳过所有 DB 依赖模块（结构化记忆、状态栏、追踪、章节、仪表盘、生命周期等），无状态模块正常加载。`,
      );
    }

    // 模块清单（v5.6 新增 tier 字段）：
    // tier 1 = 常驻层（最高 ROI，任何时候都暴露）
    // tier 2 = 均衡层（常用但非必须，默认启用）
    // tier 3 = 完整层（专业场景，minimal/balanced 下不暴露）
    // 非工具类模块（仪表盘、通知、自检、prompt-enhancer、kb-corpus）标 tier 1：它们不占工具 schema，不影响 per-turn 成本。
    const modules: Array<{ name: string; tier: Tier; enabled: boolean; load: () => void }> = [
      // ── 工具模块（占 tool schema）──
      {
        name: "结构化记忆",
        tier: 1,
        enabled: config.memory?.enabled !== false && dbAvailable,
        load: () => registerStructuredMemory(api, config.memory),
      },
      {
        name: "状态栏",
        tier: 1,
        enabled: config.statusline?.enabled !== false && dbAvailable,
        load: () => registerStatusline(api, db!, notifyQueue!),
      },
      {
        name: "子任务派发",
        tier: 1,
        enabled: true,
        load: () => registerSpawnTask(api),
      },
      {
        name: "模式闸门",
        tier: 1,
        enabled: config.mode?.enabled === true && dbAvailable,
        load: () => registerModeGate(api, config.mode, notifyQueue!),
      },
      {
        name: "技能安装器",
        tier: 1,
        enabled: true,
        load: () => registerSkillInstaller(api),
      },
      {
        name: "记忆整合",
        tier: 1,
        enabled: config.memory?.enabled !== false && dbAvailable,
        load: () => registerMemoryIntegrator(api, config.contextPruner),
      },
      {
        name: "章节标记",
        tier: 2,
        enabled: config.chapters?.enabled !== false && dbAvailable,
        load: () => registerChapterMarks(api),
      },
      {
        name: "任务追踪",
        tier: 2,
        enabled: config.todos?.enabled !== false && dbAvailable,
        load: () => registerTodoTracker(api, notifyQueue!),
      },
      {
        name: "定时任务桥",
        tier: 2,
        enabled: config.scheduledTasks?.enabled !== false && dbAvailable,
        load: () => registerScheduledTasksBridge(api),
      },
      {
        name: "历史会话搜索",
        tier: 2,
        enabled: config.transcriptSearch?.enabled !== false,
        load: () => registerTranscriptSearch(api),
      },
      {
        name: "工作流自动化",
        tier: 3,
        enabled: config.workflows?.enabled !== false,
        load: () => registerWorkflowHooks(api, config.workflows),
      },
      {
        name: "工具安全",
        tier: 3,
        enabled: config.safety?.enabled !== false && dbAvailable,
        load: () => registerToolSafety(api, config.safety),
      },
      {
        name: "任务规划",
        tier: 3,
        enabled: true,
        load: () => registerTaskPlanner(api),
      },
      {
        name: "会话回顾",
        tier: 3,
        enabled: config.sessionRecap?.enabled !== false && dbAvailable,
        load: () => registerSessionRecap(api, config.sessionRecap),
      },
      {
        name: "技能巡检",
        tier: 3,
        enabled: true,
        load: () => registerSkillDoctor(api),
      },

      // ── 非工具模块（不占 tool schema，tier 不影响）──
      {
        name: "提示词增强",
        tier: 1,
        enabled: config.prompt?.enabled !== false,
        load: () => registerPromptEnhancer(api, config.prompt),
      },
      {
        name: "输出自检",
        tier: 1,
        enabled: config.selfCheck?.enabled !== false && dbAvailable,
        load: () => registerSelfCheck(api, config.selfCheck),
      },
      {
        name: "仪表盘",
        tier: 1,
        enabled: config.dashboard?.enabled !== false && dbAvailable,
        load: () => registerDashboard(api, config.dashboard, notifyQueue!, db!),
      },
      {
        name: "共享知识库语料",
        tier: 1,
        enabled: config.kbCorpus?.enabled !== false,
        load: () => registerKbCorpus(api, config.kbCorpus),
      },
      {
        // v5.7.3: 启动期诊断 ~/.openclaw/openclaw.json 陷阱配置
        // tier=1，minimal 也启用——这是关键的 'Context limit exceeded' 兜底诊断
        name: "配置诊断",
        tier: 1,
        enabled: config.configDoctor?.enabled !== false && dbAvailable,
        load: () => registerConfigDoctor(api, config.configDoctor, notifyQueue!),
      },
      {
        // v5.7.16: 启动期诊断 trajectory.jsonl 体量
        // tier=1，minimal 也启用——超大 trajectory 会让 gateway sessions.list 卡 13s+ event-loop / 99% CPU
        // v5.7.18: 解除 dbAvailable 依赖——本模块不读 db，notifyQueue 缺失时也能跑（logger only）
        name: "trajectory 体量诊断",
        tier: 1,
        enabled: config.sessionDoctor?.enabled !== false,
        load: () => registerSessionDoctor(api, config.sessionDoctor, notifyQueue),
      },
      {
        // v5.7.20: trajectory 自动归档（输出 LaunchAgent 部署 cliCmd）
        // tier=1，minimal 也启用——零 db 依赖，纯 cliCmd 输出
        // 配合 session-doctor：诊断告警 + 一次性部署 launchd 自动归档 = 治本预防机制
        name: "trajectory 自动归档",
        tier: 1,
        enabled: config.trajectoryArchiver?.enabled !== false,
        load: () => registerTrajectoryArchiver(api, config.trajectoryArchiver),
      },
      {
        // v5.7.5: 按用户需求挑已装 skill / 推荐未装 / 给自建规划
        // tier=2 balanced 默认启用；minimal 不暴露（用户多半已经知道用啥 skill）
        name: "技能推荐",
        tier: 2,
        enabled: config.skillRecommender?.enabled !== false,
        load: () => registerSkillRecommender(api, config.skillRecommender),
      },
      {
        // v5.7.7: 接入 openclaw 4.22 的 session_start/end/before_reset/subagent_* hook
        // tier=1 minimal 也启用——这是核心生命周期补全，零工具 schema（纯 hook 监听）
        name: "会话生命周期",
        tier: 1,
        enabled: config.sessionLifecycle?.enabled !== false && dbAvailable,
        load: () => registerSessionLifecycle(api, config.sessionLifecycle, notifyQueue!),
      },
      {
        // v5.7.10: 主动 surface 龙虾原生 .md memory 文件锚点
        // tier=1 minimal 也启用——零工具 schema（纯 before_prompt_build hook）+ 解决"第二天失忆"
        name: "原生记忆 surface",
        tier: 1,
        enabled: config.nativeMemorySurfacer?.enabled !== false,
        load: () => registerNativeMemorySurfacer(api, config.nativeMemorySurfacer),
      },
      {
        // v5.7.12 实现 / v5.8.3 真接入：模型路由器（before_model_resolve hook）
        // tier=1 minimal 也启用——零工具 schema（纯 hook），按 prompt 复杂度 + 多模态自动路由
        // 5/2 实战发现：5.7.12 起 model-router 一直未接 index.ts，是"幽灵模块"
        // 5.8.3 改 sidus priority 1 → 4（兜底），deepseek 直连 priority 1（首选）
        // 触发：sidus deepseek-v4-flash 反复 429 限流卡蓝火 wecom 长任务 12 分钟+
        name: "模型路由器",
        tier: 1,
        enabled: config.modelRouter?.enabled !== false,
        load: () => registerModelRouter(api),
      },
      {
        // v5.7.22: BOT 文件分享桥（企微/钉钉无法直传大文件时的兜底）
        // tier=1 minimal 也启用——这是渠道兜底能力，没了它播客/大附件就发不出去
        // 默认 enabled=true，零 child_process（fs.copyFileSync），路径黑名单 sanitizer 防 LLM path traversal
        name: "BOT 文件分享",
        tier: 1,
        enabled: config.botShare?.enabled !== false,
        load: () => registerBotShareLink(api, config.botShare),
      },
      {
        // v6.5.3: 上下文守护（Context Watchdog）
        // hook llm_output 累加 token usage，70%/85%/95% 三阶预警 banner，
        // ≥80% 且当前 model ctx<256K 时附带"切大 ctx 模型"建议。
        // hook after_compaction 自动归零。enhance_ctx_status 工具让 LLM 主动查。
        // 龙虾原生在 overflow 错误后才走 model-fallback；本模块在错误前预警让 LLM 主动收尾。
        // tier=1 minimal 也启用——纯观察 + prompt supplement，零 child_process / 零工具开销
        name: "上下文守护",
        tier: 1,
        enabled: config.contextWatchdog?.enabled !== false,
        load: () => registerContextWatchdog(api, config.contextWatchdog),
      },
      {
        // v6.5.2: BOT 文件上传桥（用户 → AI 反向兜底，token 化基建）
        // 与 bot-share-link 镜像对称：share=出站下载，upload=入站上传。
        // 触发：企微 ≤100MB 限制无法回传给 LLM；用户拿 token URL 浏览器上传任意大小（≤2GB），
        // LLM 用 enhance_upload_check 拉清单。零新依赖（fetch+octet-stream，不引 multer/busboy）。
        // 与 large-file-bridge 并行：那个是"hook 检测错误文本→提示链接"，这个是"token 隔离基建"
        name: "BOT 文件上传",
        tier: 1,
        enabled: config.botUpload?.enabled !== false,
        load: () => registerBotUploadLink(api, config.botUpload, config.botShare),
      },
      {
        // v5.7.26: 跨 reset 自动桥接上次会话末尾对话（修复 5/2 zhaobo 失忆事故）
        // tier=1 minimal 也启用——纯 before_prompt_build hook 零工具 schema，只读 sessions/，
        // 是 session-recap（结构化元数据）+ session-lifecycle（reset 时抢救）的补盲
        name: "会话桥接",
        tier: 1,
        enabled: config.sessionBridge?.enabled !== false,
        load: () => registerSessionBridge(api, config.sessionBridge),
      },
      {
        // v5.8.0: hook-profiler 量化 OpenClaw 端到端首字延迟
        // tier=1 minimal 也启用——log-tailer + 1 个工具，零行为侵入
        // 实测痛点：用户首字延迟 p50=9.9s/p95=38.8s 不知慢在哪
        name: "hook 性能诊断",
        tier: 1,
        enabled: config.hookProfiler?.enabled !== false && dbAvailable,
        load: () => registerHookProfiler(api, openclawHome, config.hookProfiler),
      },
      {
        // v6.1.5: 蓝火 / cc-media-bridge dashboard 引导
        // tier=1 minimal 也启用——单一 prompt supplement 注入，零工具/零 hook，
        // capability detection by filesystem path（不强 require cc-media-bridge 装）
        name: "蓝火 dashboard 引导",
        tier: 1,
        enabled: config.ccBridgePrompt?.enabled !== false,
        load: () => registerCcBridgePrompt(api),
      },
      {
        // v6.x: 蓝火预查询 hook（真 harness 反幻觉）
        // before_prompt_build 检测"蓝火+任务/列表/历史"模式 → 自动 fetch /cc-sessions
        // 把真实数据注入 system prompt 作为 prependContext，LLM 不需"决定要不要调工具"
        // = 杜绝 hallucinate cc-YYYYMMDD task ID 编造列表
        name: "蓝火预查询 (反幻觉)",
        tier: 1,
        enabled: config.ccBridgePreFetch?.enabled !== false,
        load: () => registerCcBridgePreFetch(api),
      },
      {
        // v6.x: 蓝火派活 harness（强制真原生 CC 会话）
        // before_prompt_build 检测"蓝火+动词"模式 → 注入硬约束 + 设 90s session lockdown
        // before_tool_call 在 lockdown 窗口拦 sessions_spawn / Task / spawn_task / exec claude
        // = 钉死"蓝火 dispatch 必走 Bash cc-media-task"，杜绝 ACP/子 agent 截胡
        name: "蓝火派活 harness",
        tier: 1,
        enabled: config.ccBridgeDispatchHarness?.enabled !== false,
        load: () => registerCcBridgeDispatchHarness(api),
      },
      {
        // v6.5.1: 蓝火智能体关键词触发器（"封装 cc 为智能体" 用户决断版）
        // 用户发"蓝火 X" / "@蓝火 X" → hook 直接 HTTP POST cc-media-bridge:18790/dispatch
        // 桥 spawn cc-media-task 真派活 → 立即返 task_id → hook 让 LLM 只 echo 结果
        // **完全绕开 LLM 决策**：蓝火 = 独立 HTTP 服务，关键词命中即真派活
        name: "蓝火智能体关键词触发器",
        tier: 1,
        enabled: config.ccBridgeKeywordDispatch?.enabled !== false,
        load: () => registerCcBridgeKeywordDispatch(api),
      },
      {
        // v6.x: 大文件上传桥接（企微 >100MB 文件错误检测 + 上传链接引导 + 上传表单）
        // tier=2 balanced 默认启用——纯 before_prompt_build hook + 按需工具 enhance_upload_large_file
        // 与 bot-share-link 互补（后者负责文件→链接转换，本模块负责检测+上传入口）
        name: "大文件上传桥接",
        tier: 2,
        enabled: config.largeFileBridge?.enabled !== false,
        load: () => registerLargeFileBridge(api, config.largeFileBridge),
      },
      // 智能贴士已合并到小火苗模块（before_prompt_build 统一输出）
      // {
      //   name: "智能贴士",
      //   tier: 3,
      //   enabled: config.tips?.enabled !== false,
      //   load: () => { console.error("[idx] loading spinner-tips..."); registerSpinnerTips(api, config.tips, notifyQueue); },
      // },
    ];

    const loaded: string[] = [];
    const skipped: string[] = [];
    for (const mod of modules) {
      if (!mod.enabled) continue;
      if (mod.tier > maxTier) {
        skipped.push(mod.name);
        continue;
      }
      try {
        mod.load();
        loaded.push(mod.name);
      } catch (err) {
        api.logger.error(`[enhance] 模块「${mod.name}」加载失败: ${err instanceof Error ? err.message : String(err)}`);
      }
    }
    if (skipped.length > 0) {
      api.logger.info(
        `[enhance] toolTier=${toolTier}：按分层策略跳过 ${skipped.length} 个模块（${skipped.join("、")}）。改 config.toolTier = "full" 可全部启用。`,
      );
    }

    // 首次启动提示：配套技能需手动安装（插件不执行外部命令，只给提示）
    try {
      const globalSkillsDir = join(openclawHome, "workspace", "skills");
      const missing = CLAW_HUB_SKILLS.filter(
        (s) => !existsSync(join(globalSkillsDir, s)),
      );
      if (missing.length > 0) {
        api.logger.info(
          `[enhance] 检测到 ${missing.length} 个配套技能未安装：${missing.join("、")}；` +
            `调用 enhance_install_skills 获取一键安装命令，或手动运行 clawhub install <技能名> --dir ${globalSkillsDir}`,
        );
      }
    } catch {
      // 静默跳过（非关键路径）
    }

    const degradeNote = dbAvailable ? "" : "（DB 降级模式：better-sqlite3 原生绑定丢失）";
    api.logger.info(`[enhance] 龙虾增强包 v${pkg.version} 已加载（toolTier=${toolTier}，非侵入式，不重复龙虾原生功能）${degradeNote}，启用模块: ${loaded.join("、")}`);
  },
});
