# PRD-081: 结构化与高可读性的 SDLC Slack 通知机制

## 1. Context & Problem Statement
当前项目中的 Slack 通知功能（PRD-079）虽然可用，但在可读性和流程进度的体现上存在不足。现有的消息多为推送到 Slack 的纯文本日志，无法直观反映 SDLC 生命周期中各个阶段的状态，导致用户难以快速了解 PRD 或 PR 的当前进度。

## 2. User Request
用户的原始需求如下：
> “提一个小需求：现在的 sdlc 的推送很难读，理想的应该是比如
> 1.prd-xxx sdlc 启动
> 2.prd-xxx 切片中
> 3.切片结束，生成有 x 个切片
> 4.pr-1，coder 运行中
> 5.pr-1，coder 结束，review 中
> 6.pr-1，review 结果...
> 等等提现流程进度的简单更新”

## 3. Scope & Target Project
- **Target Project:** `/root/.openclaw/workspace/projects/leio-sdlc`
- **Scope:** 重构 `orchestrator.py` 中的 `notify_channel` 调用逻辑，改用带有编号、步骤指示且直观的格式（全中文）。

## 4. Solution & Feature Requirements
需要实现一套带有清晰阶段标记（Emoji）的结构化中文通知，格式参考如下（但不限于）：
- 🚀 `1. [prd-xxx] SDLC 启动`
- 🔪 `2. [prd-xxx] 切片中...`
- ✅ `3. [prd-xxx] 切片结束，共生成 [x] 个切片`
- 👨‍💻 `4. [pr-1] Coder 运行中...`
- 🧐 `5. [pr-1] Coder 结束，Review 中...`
- 📝 `6. [pr-1] Review 结果：[结果摘要]`
等等，提现整个流程进度的简单更新。

## 5. Autonomous Test Strategy
由于目标为 Python 脚本 (`orchestrator.py`)，测试策略应为：
- **Unit/Integration Testing with Mocks:** 编写针对 `orchestrator.py` 中重构后通知逻辑的单元测试。
- 使用 Mock 技术拦截并验证对 `notify_channel`（或底层 Slack API）的调用，确保发送的文本完全符合所要求的中文格式和 Emoji 标记。

## 6. TDD Guardrail
**The implementation and its failing test MUST be delivered in the same PR contract.** 开发者必须在同一 PR 中提供失败的测试（验证通知格式）以及使其通过的实现代码。
