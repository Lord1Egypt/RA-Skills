# 龙虾增强包 PRD（产品需求文档）

> 记录「**为什么做、做什么**」；「**怎么实现**」见 [architecture.md](architecture.md)。
> 滚动维护：每次新增/移除模块，补一节「需求 → 价值 → 非目标边界」。

## 1. 产品定位

**龙虾增强包（OpenClaw Enhancement Kit）** 是**非侵入式** OpenClaw 插件。在不改龙虾核心、不重复龙虾原生能力的前提下，补齐**项目工程化 + 多 Agent 运营**两个维度，让 OpenClaw 从「对话机器人」变成「可被工程化运营的 AI 助手平台」。

一句话：**龙虾有的让龙虾管，龙虾没有的我来补。**

## 2. 目标用户与场景

| 用户 | 场景 | 核心诉求 |
|---|---|---|
| job zhao（主） | 企微/服务号 AI 助手运营 | 结构化记忆、任务追踪、配置体检、文件分享预览 |
| 接手的其他 Claude 账号 | clone 即接续开发 | CLAUDE.md + docs 自带上下文 |
| 第三方 OpenClaw 用户 | npm/ClawHub 安装 | 开箱即用、单装即降级可用、不与龙虾打架 |

多 Agent 是一等公民：所有能力按 `ctx.agentId` 隔离。

## 3. 能力分组（为什么做）

- **结构化记忆**：补龙虾向量记忆之外的「带类型/字段」结构化条目；`native-memory-surfacer` 浮现原生记忆**不重复存储**。
- **项目工程化**：todo / 章节 / 会话回顾 / 轨迹归档 / 转录搜索 —— 龙虾原生都没有。
- **体检与自愈建议（诊断不修复）**：config/skill/session-doctor 扫红线给 cliCmd 建议，永不替用户改配置。
- **文件与跨端桥接**：share/upload-link、large-file-bridge 解决「LLM 生成的本地 URL 在企微 404」；**v6.7.19 起分享链接返回可预览 Markdown**（图片内联缩略图 / 文件下载卡片，龙虾管家渲染）。
- **上下文守护**：context-watchdog 在 ctx 逼近上限时预警 + 超限保护切换（防 overflow 崩溃）。
- **安全闸门**：tool-safety、mode-gate。

## 4. 设计原则（产品级约束）

1. **非侵入**：只用 SDK 公开 API，不改龙虾仓库。
2. **不重复**：加功能前先 grep `openclaw-source` 找原生等价物。
3. **单装可用**：跨插件协作走文件系统契约，缺协作方时降级。
4. **诊断不修复**：建议改配置 → return-cliCmd。
5. **零 child_process**：外部命令一律 return-cliCmd（企业扫描器红线）。
6. **分层加载**：toolTier 控制 tool schema 体量。

## 5. 非目标（Non-Goals）

- ❌ 不重复龙虾已有：记忆向量库、cron 调度、技能安装执行、tool 截断、权限 allow/deny。
- ❌ 不修改 openclaw 核心、不 push 龙虾仓库。
- ❌ 不在插件内嵌 skill 内容（skill 独立发版，插件只引用 slug）。
- ❌ 不用 child_process 执行安装/CLI。
- ❌ 不替用户判断「附件内容是否相符」等越权决策。
- ❌ **不自动替用户切换模型**（v6.7.19 起移除 model-router）—— 模型选择交回龙虾原生 / 用户配置；仅保留 context-watchdog 的超限保护切换。

## 6. 里程碑

按 [CHANGELOG.md](../CHANGELOG.md) 滚动记录。关键节点：
- v5.x：toolTier 分层、config-doctor、三层记忆/KB 协调。
- v6.0.0：包改名 `@huo15/openclaw-enhance` → `@huo15/huo15-openclaw-enhance`。
- v6.6.8：全模块 hook 防御性包裹（wrapApiForSafeHooks）。
- **v6.7.19**：去掉自动切换模型（model-router）+ 分享链接 Markdown 预览 + 适配 openclaw 2026.6.10（修 definePluginEntry TS2742）。

## 7. 迭代节奏

每 3 天自我迭代一轮，判定标准与 fast-track 见 [SELF_ITERATE.md](SELF_ITERATE.md)。
