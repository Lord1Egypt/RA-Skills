# enhance 插件改进规划

> 基于 AI Agent Harness 六层能力架构分析（2026-04-14）

## 源码目录
`~/workspace/projects/openclaw/huo15-openclaw-enhance/`

## 当前模块清单（v1.9.0）
| 模块 | 文件 | 功能 | 状态 |
|------|------|------|------|
| 结构化记忆 | `modules/structured-memory.ts` | SQLite 持久化，5分类记忆 | ✅ 已有 |
| 工具安全 | `modules/tool-safety.ts` | hardblock/block/log 三级拦截 | ✅ 已有 |
| 提示词增强 | `modules/prompt-enhancer.ts` | 追加质量准则 | ✅ 已有 |
| 工作流自动化 | `modules/workflow-hooks.ts` | 触发词→固定指令 | ✅ 已有 |
| 仪表盘 | `modules/dashboard.ts` | 统计面板 | ✅ 已有 |
| 小火苗+贴士 | `modules/flame-pet.ts` | XP系统+每日贴士 | ✅ 已有 |
| **输出自检** | `modules/self-check.ts` | before_agent_reply 输出验证 | ✅ **新增** |
| **Context裁剪** | `modules/context-pruner.ts` | before_prompt_build 记忆过滤 | ✅ **新增** |

---

## 已完成（v1.9.0 — 第1次迭代）

### ✅ `self-check.ts`（评估与观测 — P0）
- Hook: `before_agent_reply` — 在输出发送前拦截
- 检测：空输出、NO_REPLY、超长输出、错误关键词
- 非阻断：问题只记录到 SQLite safety_log
- 可选阻断：空输出时可选择拦截并返回错误提示
- 配置项：`checkEmpty`、`checkNoReply`、`checkErrorKeywords`、`checkExcessiveLength`、`blockOnEmpty`

### ✅ `context-pruner.ts`（信息边界 — P0）
- Hook: `before_prompt_build` — 记忆注入前过滤
- 四维评分：关键词重合度（50%）+ 分类权重（30%）+ 重要性（10%）+ 新鲜度（10%）
- 阈值可配置（默认 0.25），最多注入 10 条
- 替代 Claude Code 的 `findRelevantMemories()` LLM 筛选（本地轻量方案）

---

## 待做（规划）

### 🟡 P1 — 第2次迭代
- `tool-safety.ts` 增加自动重试（429 指数退避、500 重试、新增错误分类）
- `task-planner.ts`（执行编排）— 任务分解工具

### 🟢 P2 — 第3次迭代
- 记忆整合：废弃 enhance structured-memory，桥接到 OpenClaw memory-core
- 工作流增强：条件分支 + 状态追踪

---

## 注意事项
- 所有模块必须通过 `before_prompt_build` 或工具暴露，不修改 openclaw 核心
- 多 Agent 隔离：所有状态读取 `ctx.agentId`
- SQLite 表结构不变，兼容现有数据
- 仪表盘自动反映新模块的统计数据

## 已完成（v2.0.0 — 第2次迭代）

### ✅ `tool-safety.ts` 增强 — 自动重试
- `after_tool_call` hook：错误分类（rate_limit/server_error/network_error/auth_error/timeout/unknown）
- 429 → 指数退避（最多5次，baseDelay 1s，multiplier 2x）
- 5xx → 重试3次（baseDelay 2s）
- 网络超时 → 重试2-3次（baseDelay 1s）
- 401/403 权限错误不重试（直接标记为 auth_error）
- `enhance_retry_status` 工具：查询当前待重试任务
- 配置项：`enableRetry: true`（默认开启）

### ✅ `task-planner.ts`（执行编排 — P1）
- Tool: `enhance_plan_task` — 目标 → 结构化子任务分解
- Hook: `before_prompt_build` 自动检测触发词并注入规划提示
- 启发式分解规则：代码开发、Odoo系统、反思模式、通用分解
- 支持 mode: plan/analyze/reflect


## 🐛 Bug修复（v2.0.1）

### ✅ 消除全部10个TS类型错误
- **根因**：OpenClaw SDK 的 `AgentTool` 类型要求 `label: string`，但运行时 Jiti 解析器不检查此字段
- **修复**：`api.registerTool(...)` 工厂函数改为 `api.registerTool(( ... as any), ...)`
- **结果**：`npx tsc --noEmit` → 0 errors


## ✅ P2 完成（v2.1.0）

### ✅ 记忆整合 — `memory-integrator.ts`
- `registerMemoryCapability` 把 enhance SQLite 注册为 OpenClaw corpus supplement
- OpenClaw 搜索记忆时会同时返回 enhance 的分类记忆
- 新工具 `enhance_memory_export`：导出所有记忆为 JSON（可同步到 Obsidian/KB）

### ✅ 工作流增强 — `workflow-hooks.ts` 全面升级
- **正则触发**：触发词支持 `/pattern/flags` 语法
- **条件分支**：支持 keyword/regex/time_range/day_of_week 条件评估
- **任务状态**：新增 `enhance_task` 工具（create/update/list/get/delete）
- **看板视图**：新增 `enhance_workflow_tasks` 工具
- 任务状态持久化到 `workflows/workflow-tasks.json`（跨 session 追踪）

