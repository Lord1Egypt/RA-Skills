/**
 * 模块: 任务规划器（Task Planner）
 *
 * Tool: enhance_plan_task
 * Hook: before_prompt_build
 *
 * 功能：
 * - 将用户的复杂目标分解为可执行的子任务列表
 * - 提供结构化的任务描述（目标、步骤、优先级、预计工时）
 * - 在检测到"帮我做"/"规划"/"分析一下"等触发词时自动注入规划提示
 *
 * 对标 Claude Code "执行编排" 能力（Agent Harness 六层第3层）
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";

// ── 类型 ──
export interface SubTask {
  id: string;
  title: string;
  description: string;
  priority: "high" | "medium" | "low";
  estimatedMinutes?: number;
  dependencies: string[]; // 依赖的子任务 id
  status: "pending" | "in_progress" | "completed";
}

export interface TaskPlan {
  goal: string;
  tasks: SubTask[];
  summary: string;
  totalEstimatedMinutes?: number;
}

// ── 任务分解提示词 ──
const TASK_DECOMPOSITION_PROMPT = `你是一个专业的任务规划助手。请将用户的复杂目标分解为具体的可执行子任务。

分解原则：
1. 每个子任务应该是原子性的（单一职责）
2. 按执行顺序排列，考虑依赖关系
3. 为每个任务标注优先级：高(HIGH)/中(MEDIUM)/低(LOW)
4. 估计每个任务的耗时（分钟）
5. 识别跨agent协作机会（如需要写代码+测试+部署，拆分为独立任务）

输出格式（严格 JSON）：
{
  "goal": "用户目标的简短描述",
  "tasks": [
    {
      "id": "task-1",
      "title": "任务标题",
      "description": "具体要做什么",
      "priority": "HIGH|MEDIUM|LOW",
      "estimatedMinutes": 30,
      "dependencies": [],
      "status": "pending"
    }
  ],
  "summary": "整体计划的一句话总结",
  "totalEstimatedMinutes": 总分钟数
}`;

// ── 触发词 ──
const TRIGGER_PATTERNS = [
  /帮我做/i,
  /帮我处理/i,
  /帮我完成/i,
  /帮我规划/i,
  /规划一下/i,
  /计划一下/i,
  /怎么实现/i,
  /如何实现/i,
  /如何做/i,
  /分析一下/i,
  /完整方案/i,
  /具体步骤/i,
  /执行方案/i,
  /从零开始/i,
  /整体方案/i,
  /TODO/i,
  /\(分解\)/i,
];

const REFLECTION_PATTERNS = [
  /反思一下/i,
  /回顾一下/i,
  /总结一下/i,
  /评估一下/i,
];

// ── 执行 ──
function extractGoalFromQuery(query: string): string {
  // 去掉触发词，得到核心目标
  let goal = query
    .replace(/帮我做|帮我处理|帮我完成|帮我规划|规划一下|计划一下|怎么实现|如何实现|如何做|分析一下|完整方案|具体步骤|执行方案|从零开始|整体方案/g, "")
    .trim();
  return goal || query.slice(0, 100);
}

function generateTaskId(index: number): string {
  return `task-${String(index + 1).padStart(2, "0")}`;
}

// ── 主模块 ──
export function registerTaskPlanner(api: OpenClawPluginApi) {

  // ── Tool: enhance_plan_task ──
  // 注意: 工厂函数类型在运行时通过 Jiti 解析，TS 类型仅为编译参考
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  api.registerTool( (
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_plan_task",
      description: "将复杂目标分解为可执行子任务列表（用于规划/分析/反思）",
      parameters: Type.Object({
        goal: Type.String({ description: "目标或问题描述" }),
        constraints: Type.Optional(
          Type.String({ description: "约束条件（时间/技术栈等）" }),
        ),
        mode: Type.Optional(
          Type.Union([Type.Literal("plan"), Type.Literal("analyze"), Type.Literal("reflect")], {
            description: "plan|analyze|reflect",
            default: "plan",
          }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>): Promise<any> {
        const goal: string = (params.goal as string) ?? "";
        const constraints: string = (params.constraints as string) ?? "";
        const mode: string = (params.mode as string) ?? "plan";

        if (!goal.trim()) {
          return {
            content: [
              {
                type: "text" as const,
                text: "⚠️ 请提供目标描述。例如：`帮我完成 Odoo 数据库迁移`",
              },
            ],
          };
        }

        const agentId = (ctx as any)?.agentId ?? "main";

        // 构建分解请求
        const fullGoal = [goal, constraints].filter(Boolean).join("\n约束: ");

        // 模拟任务分解（基于启发式规则，简单场景直接分解）
        // 实际生产中可接入 LLM API 做真实分解
        const tasks = decomposeGoal(fullGoal, mode);

        // 渲染输出
        const planText = renderTaskPlan(tasks, goal);

        api.logger.info(`[enhance-taskplanner] 生成了 ${tasks.tasks.length} 个子任务 (agent: ${agentId})`);

        return {
          content: [{ type: "text" as const, text: planText }],
        };
      },
    }) as any),
    { name: "enhance_plan_task" },
  );

  // ── Hook: before_prompt_build — 自动触发规划 ──
  api.on("before_prompt_build", (event: any, ctx: any) => {
    const query: string = (event as any)?.prompt ?? "";
    const agentId = (ctx?.agentId ?? "main") as string;

    // 检测触发词
    const isPlanningIntent = TRIGGER_PATTERNS.some((p) => p.test(query));
    const isReflectionIntent = REFLECTION_PATTERNS.some((p) => p.test(query));

    if (!isPlanningIntent && !isReflectionIntent) return {};

    const mode = isReflectionIntent ? "reflect" : "plan";
    const goal = extractGoalFromQuery(query);

    // 注入任务分解提示
    const injection = [
      "\n\n<!-- enhance-taskplanner: 自动任务规划 -->",
      isReflectionIntent
        ? "【反思模式】请先总结当前状态，然后识别改进机会：\n"
        : "【任务规划】请将以下目标分解为具体可执行的子任务：\n",
      `目标: ${goal}`,
      "\n分解要求：",
      "1. 每个子任务原子化（单一职责）",
      "2. 按执行顺序排列，标注依赖",
      "3. 优先级：高(H)/中(M)/低(L)",
      "4. 估计耗时（分钟）",
      `\n输出格式：使用 enhance_plan_task 工具，mode="${mode}"`,
    ].join("\n");

    return { prependContext: injection };
  });

  api.logger.info("[enhance] 任务规划模块已加载（enhance_plan_task tool + before_prompt_build 自动触发）");
}

// ── 启发式任务分解 ──
function decomposeGoal(goal: string, mode: string): TaskPlan {
  const goalLower = goal.toLowerCase();

  // 简单分解规则
  if (mode === "reflect") {
    return {
      goal,
      summary: "当前状态反思与改进计划",
      totalEstimatedMinutes: 15,
      tasks: [
        { id: "task-01", title: "总结当前进展", description: "列出已完成的关键里程碑和当前状态", priority: "high", estimatedMinutes: 5, dependencies: [], status: "pending" },
        { id: "task-02", title: "识别问题与风险", description: "列出当前面临的主要问题和潜在风险", priority: "high", estimatedMinutes: 5, dependencies: ["task-01"], status: "pending" },
        { id: "task-03", title: "制定改进计划", description: "针对识别出的问题，制定具体的改进措施", priority: "medium", estimatedMinutes: 5, dependencies: ["task-02"], status: "pending" },
      ],
    };
  }

  // 代码开发类任务
  if (goalLower.includes("开发") || goalLower.includes("实现") || goalLower.includes("写代码") || goalLower.includes("coding")) {
    return {
      goal,
      summary: "代码开发完整流程",
      totalEstimatedMinutes: 120,
      tasks: [
        { id: "task-01", title: "需求分析", description: "明确功能需求、输入输出、边界条件", priority: "high", estimatedMinutes: 15, dependencies: [], status: "pending" },
        { id: "task-02", title: "技术方案设计", description: "选择技术栈、设计数据结构、定义接口", priority: "high", estimatedMinutes: 20, dependencies: ["task-01"], status: "pending" },
        { id: "task-03", title: "编写代码", description: "按设计方案实现功能代码", priority: "high", estimatedMinutes: 60, dependencies: ["task-02"], status: "pending" },
        { id: "task-04", title: "单元测试", description: "编写并运行单元测试，验证核心逻辑", priority: "high", estimatedMinutes: 15, dependencies: ["task-03"], status: "pending" },
        { id: "task-05", title: "集成测试", description: "将新代码与现有系统集成，验证端到端流程", priority: "medium", estimatedMinutes: 10, dependencies: ["task-04"], status: "pending" },
      ],
    };
  }

  // Odoo 相关任务
  if (goalLower.includes("odoo") || goalLower.includes("ERP")) {
    return {
      goal,
      summary: "Odoo 系统任务执行计划",
      totalEstimatedMinutes: 90,
      tasks: [
        { id: "task-01", title: "环境检查", description: "确认 Odoo 版本、数据库连接、依赖状态", priority: "high", estimatedMinutes: 5, dependencies: [], status: "pending" },
        { id: "task-02", title: "数据备份", description: "在操作前备份数据库和附件文件", priority: "high", estimatedMinutes: 10, dependencies: ["task-01"], status: "pending" },
        { id: "task-03", title: "需求分析", description: "理解业务需求，确定改动范围", priority: "high", estimatedMinutes: 15, dependencies: ["task-01"], status: "pending" },
        { id: "task-04", title: "代码/配置修改", description: "按需求修改模型、视图、工作流", priority: "high", estimatedMinutes: 40, dependencies: ["task-02", "task-03"], status: "pending" },
        { id: "task-05", title: "功能验证", description: "在测试环境验证修改效果", priority: "medium", estimatedMinutes: 15, dependencies: ["task-04"], status: "pending" },
        { id: "task-06", title: "上线部署", description: "将修改部署到生产环境", priority: "medium", estimatedMinutes: 5, dependencies: ["task-05"], status: "pending" },
      ],
    };
  }

  // 默认分解
  return {
    goal,
    summary: `完成目标所需的关键步骤`,
    totalEstimatedMinutes: 30,
    tasks: [
      { id: "task-01", title: "收集信息", description: "收集与目标相关的所有信息", priority: "high", estimatedMinutes: 5, dependencies: [], status: "pending" },
      { id: "task-02", title: "分析现状", description: "分析当前状态，识别差距", priority: "high", estimatedMinutes: 10, dependencies: ["task-01"], status: "pending" },
      { id: "task-03", title: "制定方案", description: "制定具体的执行方案", priority: "high", estimatedMinutes: 10, dependencies: ["task-02"], status: "pending" },
      { id: "task-04", title: "执行与验证", description: "按方案执行并验证结果", priority: "medium", estimatedMinutes: 5, dependencies: ["task-03"], status: "pending" },
    ],
  };
}

// ── 渲染 ──
function renderTaskPlan(plan: TaskPlan, originalGoal: string): string {
  const lines = [
    `📋 **任务计划**\n`,
    `**目标**: ${originalGoal}`,
    `**总结**: ${plan.summary}`,
    plan.totalEstimatedMinutes ? `**预计总耗时**: ~${plan.totalEstimatedMinutes} 分钟\n` : "\n",
    `---`,
    `**子任务 (${plan.tasks.length} 个)**\n`,
  ];

  for (const task of plan.tasks) {
    const priorityEmoji = task.priority === "high" ? "🔴" : task.priority === "medium" ? "🟡" : "🟢";
    const deps = task.dependencies.length > 0 ? ` ← ${task.dependencies.join(", ")}` : "";
    const time = task.estimatedMinutes ? ` (${task.estimatedMinutes}min)` : "";

    lines.push(
      [
        `**${priorityEmoji} ${task.id}** ${task.title}${time}`,
        `   └─ ${task.description}`,
        `   └─ 依赖: ${task.dependencies.length > 0 ? deps : "无"}${deps}`,
      ].join("\n"),
    );
  }

  lines.push("\n---\n💡 **提示**: 使用 `enhance_plan_task` 工具获取更详细的分解");

  return lines.join("\n");
}
