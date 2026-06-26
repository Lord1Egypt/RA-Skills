# AGENTS.md — nexum-ts
<!--
  ⚠️ AGENTS.md is the source of truth. CLAUDE.md 由 dispatch.sh 自动同步，请勿直接编辑 CLAUDE.md。
  技术规范通过 lesson → harvest 流程更新；`nexum:lessons` 区间只允许 gardener 维护。
-->

## 项目概览
- 项目：OpenNexum
- 技术栈：TypeScript, Node.js, pnpm monorepo, ACP
- 类型：coding

## 目录
- 架构说明 → ARCHITECTURE.md
- 技术设计 → docs/design/
- 踩坑记录 → docs/lessons/
- 任务合约 → docs/nexum/contracts/

## 核心规范
- 使用 Conventional Commits。
- 保持 commit 原子化；一个 commit 只做一件完整的事。
- 直接 push 到 `main`/`master`，快速迭代，出问题直接 revert。
- 未经 Contract 明确允许，不要修改 scope 之外的文件。
- 修改代码时同步维护必要测试和文档，避免提交半成品。
- 不要在未确认影响面的情况下做大范围重构。
- 所有自动生成或派生文件都必须有明确来源，不要手工维护双写状态。
- `CLAUDE.md` 为派生文件；如 `AGENTS.md` 变化，由系统同步，不要手动编辑。

## 禁止事项


## 技术层规范
<!-- nexum:lessons:start -->
<!-- 由 gardener 自动维护，请勿手动修改此区间 -->
<!-- nexum:lessons:end -->

## 错误学习协议

遇到非预见错误或值得记录的模式时：

1. 修复或完成任务
2. 写入 `docs/lessons/YYYY-MM-DD-<TASK-ID>.md`（使用 `docs/lessons/TEMPLATE.md`）
3. 不要直接修改 `AGENTS.md` 的 `nexum:lessons` 区间 — 由 gardener 统一维护
4. 不要直接编辑 `CLAUDE.md` — 由 dispatch.sh 自动同步

这是强制要求，不是可选项。
