# 架构说明（architecture.md）

> 龙虾增强包 v6.x — 非侵入式 OpenClaw 插件架构

## 1. 顶层结构

```
index.ts             插件入口（definePluginEntry → register）
src/modules/*        36 个功能模块，每个 register 一类能力
src/utils/*          共享工具：sqlite-store / safe-api-wrapper / resolve-home /
                     notification-queue / latency-tracker / route-history / model-route-config
src/types.ts         EnhancePluginConfig 等类型定义
openclaw.plugin.json 插件 manifest（config schema / contracts.tools / compat）
scripts/*            setup.sh（bin）/ release.sh / postinstall.cjs
templates/*          非嵌入式长文档模板
```

## 2. 入口流程（index.ts）

1. 静态 import 全部模块 register 函数。
2. `createRequire` 读 `package.json` 拿 version。
3. `const enhancePlugin: OpenClawPluginDefinition = definePluginEntry({ id:"enhance", register })` + `export default enhancePlugin`
   —— 具名常量 + 显式类型注解规避 SDK 2026.6.x 的 TS2742（见 docs/lessons）。
4. register 内顺序：
   - `wrapApiForSafeHooks(rawApi)` —— 拦截 `api.on()`，让**所有**模块 hook handler 自动套 try/catch；抛错只 log + return undefined，**不影响龙虾主流程**（v6.6.8 起的全局防御）。
   - `resolveOpenClawHome()` 解析 `~/.openclaw` 根目录。
   - `initDb()` 初始化 better-sqlite3；原生绑定缺失则进 **DB 降级模式**（插件照常加载）。
   - 按 `toolTier` 逐个 register 模块，收集 `loaded` 列表。
   - `api.logger.info` 打印加载汇总。

## 3. 工具分层（toolTier）

`index.ts` 的 `TIER_MAX`：`minimal→1`、`balanced→2`（默认）、`full→3`。每个模块标 tier，运行时**只 register tier ≤ 当前档位的模块**，其余整个不加载（省 tool schema 重量）。

## 4. 模块清单（src/modules/，36 个）

### 记忆与上下文
| 模块 | 职责 |
|---|---|
| `structured-memory.ts` | 结构化记忆：按 agentId 隔离增删改查，注册 `enhance_memory_*` + memory capability |
| `memory-integrator.ts` | 把外部记忆源桥接进结构化记忆 |
| `native-memory-surfacer.ts` | 把龙虾**原生** memory 结果在合适时机浮现，不重复存储 |
| `kb-corpus.ts` | 把 `~/.openclaw/kb/shared/wiki` 挂为 memory corpus supplement |
| `prompt-enhancer.ts` | registerMemoryPromptSupplement 注入质量准则段 |
| `context-watchdog.ts` | 上下文守护：70/85/95% 预警 banner；95% 超限时强切大 ctx 模型防 overflow；手动切换工具 |

### 任务与会话工程化
| 模块 | 职责 |
|---|---|
| `task-planner.ts` | 多步任务计划与进度 |
| `todo-tracker.ts` | todo 持久化追踪（补龙虾没有的） |
| `chapter-marks.ts` | 会话章节标记（呼应原生 mark_chapter） |
| `spawn-task.ts` | 后台任务派生，return-cliCmd |
| `session-recap.ts` | idle 后汇总会话要点 |
| `session-lifecycle.ts` | 监听 session 开始/结束 |
| `session-bridge.ts` | 跨会话/跨设备接续（蓝火 cc-XXX） |
| `transcript-search.ts` | 在归档 jsonl 里检索历史对话 |
| `trajectory-archiver.ts` | trajectory 镜像归档 |

### 体检与诊断（诊断不修复）
| 模块 | 职责 |
|---|---|
| `self-check.ts` | 验证插件自身配置/依赖 |
| `config-doctor.ts` | 扫已装插件 compat.pluginApi / tools.profile 红线 |
| `session-doctor.ts` | 诊断卡住/异常 session |
| `skill-doctor.ts` | 扫已装 skill frontmatter/slug 一致性 |
| `skill-recommender.ts` | 按上下文推荐 skill |
| `hook-profiler.ts` | 统计 hook handler 耗时 |

### 文件与桥接
| 模块 | 职责 |
|---|---|
| `bot-share-link.ts` | `enhance_share_file/list/revoke`：生成下载 URL；**v6.7.19 起返回可预览 Markdown**（图片 `![](url)` 内联缩略图 / 文件 `[📎](url)` 下载卡片） |
| `bot-upload-link.ts` | 生成上传 token URL |
| `large-file-bridge.ts` | 弱模型兜底生成上传/下载 token URL，零依赖 |
| `cc-bridge-prompt.ts` / `cc-bridge-pre-fetch.ts` / `cc-bridge-dispatch-harness.ts` / `cc-bridge-keyword-dispatch.ts` | Claude Code 桥接：prompt 段 / 预取 / 事件流编排 / 关键词触发（蓝火接续） |

### 路由 / 安全 / 安装 / 展示
| 模块 | 职责 |
|---|---|
| `tool-safety.ts` | 工具调用日志、风险分级、危险命令拦截建议 |
| `mode-gate.ts` | 按运行模式 gate 工具可用性 |
| `workflow-hooks.ts` | on(hook) 事件驱动自动化 |
| `skill-installer.ts` | 生成 `clawhub install` 命令，return-cliCmd |
| `scheduled-tasks-bridge.ts` | 桥接 openclaw cron，return-cliCmd |
| `statusline.ts` | statusline 贡献 |
| `dashboard.ts` | HTTP 路由展示各模块状态 |
| `notification-queue.ts` | 异步通知派发（被其他模块复用） |

> **已移除**：`model-router.ts`（自动切换模型）在 v6.7.19 删除。其曾用的 `latency-tracker` / `route-history` / `model-route-config` 工具**保留**，因为 context-watchdog 的 `isModelBanned` 仍依赖；ban 列表无人填充后该检查变 no-op，无害。详见 [decisions/0002-remove-model-router.md](decisions/0002-remove-model-router.md)。

## 5. 数据流与存储

- **SQLite**（better-sqlite3）：库在 `~/.openclaw` 下，根目录由 `resolve-home.ts` 决定；`sqlite-store.ts` 的 `initDb()` 建表，原生绑定缺失降级。
- **KB 语料**：读 `~/.openclaw/kb/shared/wiki/*.md` 经 `registerMemoryCorpusSupplement` 桥接进 memory。
- **归档**：会话 jsonl / trajectory 镜像到持久目录。
- **隔离**：记忆/日志/工作流全部按 `ctx.agentId` 隔离 —— 适配企微动态 Agent。

## 6. 非侵入边界（与龙虾的契约）

- 只用 SDK 公开 API（`api.on` / `api.register*` / `api.logger` / HTTP 路由 / capability 注册），不 import 龙虾内部模块。
- 所有 hook 经 `wrapApiForSafeHooks` 包裹，保证插件异常不传导给龙虾。
- 跨插件协作走文件系统契约，单装也能降级运行。
