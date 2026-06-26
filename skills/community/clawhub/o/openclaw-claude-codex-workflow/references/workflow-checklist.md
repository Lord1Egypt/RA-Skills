# 工作流检查清单

使用本清单确保 ccg-workflow 风格的六阶段流程在 OpenClaw 内保持一致性。每个阶段都需要更新 `.claude/` 目录下的工件，并在 Git 分支说明里引用阶段进度。

## Phase 0：Context Capture
- [ ] 运行 `claude run scripts/ccg_orchestrator.sh plan` 前，确认 `git status` 纯净。
- [ ] 将用户输入、OPSX ticket、spec 摘要写入 `.claude/context.md`。
- [ ] 如果缺少关键事实，记录在 `.claude/questions.md` 并反馈给请求方。
- [ ] 用 `jq` 校验任何 JSON Prompt，避免 Claude 误读。

## Phase 1：OPSX / Scope Alignment
- [ ] Claude 读取 `.claude/context.md`，输出 `.claude/scope.md`，明确后端 / 前端 / 集成需求。
- [ ] 标注需要 Codex 或 Gemini 介入的路径，为决策树输入。
- [ ] 在 scope 中列出安全约束（不可写目录、需要审批的命令）。
- [ ] 若任务映射到现有 spec/ADR，链接并抄写关键段落。

## Phase 2：Plan（Decision + Hooks）
- [ ] 运行 `scripts/ccg_orchestrator.sh <plan-file> --backend '<prompt>' --frontend '<prompt>'` 生成 `.claude/plan.md`。
- [ ] 在 plan 中包含 Phase 3 的任务表、owner（Codex/Gemini）、估计命令（`codex exec`, `gemini run` 等）。
- [ ] 更新 `.claude/hooks.md` 描述 orchestrator 如何唤起 CLI（cwd、branch、env）。
- [ ] 将 references/model-routing.md 的选择理由写入 plan 结尾。

## Phase 3：Execute（Implementation）
- [ ] Codex 负责 backend-task：在 `workspace` 根开 PTY，按 plan 执行命令，日志写 `.claude/log_backend.md`。
- [ ] Gemini 负责 frontend slice：切到 `frontend/` 工作树，日志写 `.claude/log_frontend.md`。
- [ ] 每次提交前运行 `git diff --stat` 并记录在日志。
- [ ] 所有脚本调用必须通过 `scripts/ccg_orchestrator.sh` 的 helper 函数，避免散乱命令。

## Phase 4：Stabilize / Verification
- [ ] Claude 汇总 Phase 3 日志，生成 `.claude/test_matrix.md`（列出已跑/待跑测试）。
- [ ] Codex 运行回归测试（`npm test`, `pytest`, `go test`）并将结果粘贴进 `.claude/test_matrix.md`。
- [ ] Gemini 对 UI 结果截屏或描述，与仓库内 assets 对比。
- [ ] 记录任何阻塞项与 fallback 触发情况。

## Phase 5：Review / Handoff
- [ ] Claude 再次运行 orchestrator review 函数，生成 `.claude/review.md`。
- [ ] Review 包含：diff 摘要、风险、待办、Git 提交建议。
- [ ] 在 `.claude/merge_plan.md` 说明 branch 策略（主仓库 vs 工作树）。
- [ ] Merge 前由 Codex 检查 `git status`，确保只有经批准的文件发生变化。
