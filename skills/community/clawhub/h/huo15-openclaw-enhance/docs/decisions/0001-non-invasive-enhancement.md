# ADR 0001 — 非侵入式增强，不重复龙虾原生

## 决策

本插件**只补龙虾没有的能力**，绝不修改龙虾核心、不复制龙虾已有功能。

## 背景

OpenClaw（龙虾）原生已有：记忆向量库、cron 调度、技能安装、tool result 截断、权限 allow/deny、model-fallback。如果插件再造一套，会造成双账本、状态漂移、UX 撕裂。

## 约束

- 加新功能前先 `grep ~/workspace/projects/openclaw/openclaw-source` 找原生等价物。
- 原生**有** → 走原生 API（`registerMemoryCapability` / `registerCompactionProvider` / `on(hook, handler)` / `registerMemoryCorpusSupplement` 等）。
- 原生**没有** → 才补（todo 追踪、章节标记、仪表盘、workflow 触发器、qualityGuidelines prompt 段、配置体检、文件分享桥等）。
- 只用 SDK 公开 API，不 import 龙虾内部模块。
- 所有 hook 经 `wrapApiForSafeHooks` 包裹，插件异常不传导给龙虾。

## 后果

- 龙虾升级时插件受影响面小（只依赖 SDK 表面）。
- `native-memory-surfacer` 等模块负责「浮现」原生结果而非复制，体现「让龙虾管」。
