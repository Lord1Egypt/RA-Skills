# 模型路由指南

## Claude Code（策划 / 复查）
- 需要跨阶段推理、任务拆分或审查 Codex/Gemini 输出时优先使用 `claude` CLI。
- 当输入上下文嘈杂或需要整合 OPSX 规范、spec/ADR、客户约束时让 Claude 先归档成 .claude/context 与 plan。
- 想要自动生成 Phase 0-2 的 artifacts、或在 Phase 5 做 review/merge 评语时调用 Claude。
- 需要基于外部文档生成 Git 指令或 orchestrator 命令时让 Claude 产出命令草案。
- Fallback：Claude 受限或离线时，退回到 Codex 手写 plan，但必须在 SKILL.md 的流程里手工更新 .claude/plan 并加注“来自 Codex 的手写计划”。

## Codex（后端 / 基础设施实现）
- 所有需要 PTY 的指令（尤其是 `codex exec` 调用 gpt-5.3-codex）都走 `codex` CLI；默认运行在 /root/.openclaw/workspace。
- 适合处理 Phase 3 后端实现、测试、脚本编写、CI 配置、数据库/Infra 相关任务。
- 在需要 edit 多文件、执行 `rg`, `uv`, `npm`, `pytest` 等命令时使用 Codex；Claude/Gemini 只能发计划或审查。
- Claude 输出 patch 时由 Codex 在本地套用；禁止让外部模型直接写仓库。
- Fallback：Codex CLI 不可用时，Claude 只能发 patch 草图，需由真人或后续 Codex 回来时再执行。

## Gemini（前端 / UX 实现）
- 需要快速产出 React/Vite/Tailwind/UI 代码或高保真前端资源时调用 `gemini` CLI。
- 适用于 Phase 3 前端 slice、storybook 原型、Figma-to-code 转换。
- 要求 sandbox 中预先创建 `frontend/` branch/工作树，Gemini 只写该路径。
- Fallback：若 Gemini CLI 缺失，则让 Codex 负责临时前端实现，并在 Phase 4 记录“Gemini 缺席”以便后补。

## 升级与降级策略
- 模型选择以 references/workflow-checklist.md 的阶段职责为准；若某模型不可用，记录在 Phase 1 的工作日志里。
- 复杂任务优先 `claude -> codex -> gemini -> claude` 顺序。单一后端任务可跳过 Gemini，但依旧要在 Phase 2 注记。
- 任何 fallback 都需要更新 `.claude/plan`、`.claude/log`，并在 Git commit message 中引用。
