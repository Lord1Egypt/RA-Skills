---
name: openclaw-claude-codex-workflow
description: 在 OpenClaw 中需要 Claude Code 负责编排/评审、Codex 实现后端、Gemini 实现前端的多模型流水线时启用；尤其适用于需要 OPSX/spec 对齐、分阶段 artifacts、以及 claude→codex→gemini→claude 闭环交付的任务。
---

# OpenClaw Claude Codex Workflow

## 概述
- 架构：Claude Code 作为 planner/reviewer，Codex 作为具有 PTY 的后端执行者，Gemini 作为前端/UX 生成器，所有阶段通过 `.claude/` 工件与 `scripts/ccg_orchestrator.sh` 串联。
- 保障：任何写操作由 Codex/Gemini 在本地工作树执行，Claude 仅生成文本/plan；每个阶段都在 Git 干净状态下进行，并遵循 references/workflow-checklist.md 列出的清单。
- 结果：交付不只包含代码，还包括 plan、hooks、test matrix、review memo，满足 ccg-workflow 式高标准。

## Quick Start
### 前置条件
- Node.js 20+、jq、GNU coreutils；`git status` 必须干净，或显式设置 `ALLOW_DIRTY=1`。
- 安装 CLI 并验证 `claude --version`、`codex --version`、`gemini --version` 可用（Claude Code CLI、Codex CLI、Gemini CLI 官方安装方式自行遵循厂商文档）。
- 设置凭据：`CLAUDE_API_KEY`、`CODEX_API_KEY`、`GOOGLE_API_KEY` 等；在 shell profile 中 `export`，以便脚本继承。

### 安装/挂载
1. 确保仓库在 `/root/.openclaw/workspace` 或可写工作树中。
2. 将用户需求/OPSX ticket 粘贴进 `.claude/context.md`。
3. 运行 `scripts/ccg_orchestrator.sh .claude/plan.md --plan-prompt "<plan 指令>" --backend "<后端需求>" --frontend "<前端需求>" --review "<review 指令>" --context .claude/context.md`。
4. 根据输出的日志，切换到相应模型 CLI，必要时使用 `--dry-run` 先审阅命令。

### Git 规则
- 不允许外部模型写入工作区；只有 Codex/Gemini 通过本地 shell 修改文件。
- 每个阶段结束前运行 `git status` 和 `git diff --stat`，记录在 `.claude/log_backend.md` 或 `.claude/log_frontend.md`。
- 使用 `git worktree add ../frontend <branch>` 给 Gemini 独立空间，避免与 Codex 冲突。

## Workflow Decision Tree
| 场景 | 触发条件 | 主模型 | 协同模型 | 备注 |
| --- | --- | --- | --- | --- |
| 仅需策略/计划 | 用户只要拆解、无代码 | Claude | （可选）Codex | 生成 `.claude/plan.md`，停在 Phase 2 |
| 后端 API/脚本修改 | 涉及 CI、数据库、后端逻辑 | Codex | Claude | 使用 `codex exec --prompt`，Claude 复查 diff |
| UI / 视觉组件 | 新增 React/Vite/Storybook ／ CSS | Gemini | Codex | Gemini 写前端目录，Codex 处理 API mock |
| 全栈功能 | 同时触及 API + UI | Claude → Codex → Gemini → Claude | 三者互锁 | 使用 references/model-routing.md 的顺序和 fallback |
| 紧急热修 | 小范围补丁，时间敏感 | Codex | Claude | 可以跳过 Gemini，但要在 Phase 4 记录原因 |

更多启发式参阅 [references/model-routing.md](references/model-routing.md)。

## Phase 0：Context Capture
- 按 [references/workflow-checklist.md](references/workflow-checklist.md) 填写 `.claude/context.md`、`.claude/questions.md`。
- 汇总 OPSX ticket、现有 spec/ADR，标注机密与不可修改目录。
- 若资料缺口大，先用 Claude 生成提问列表，再反馈给请求方。

## Phase 1：OPSX / Scope Alignment
- 运行 `claude run --input .claude/context.md --output .claude/scope.md`（或通过 orchestrator `--plan-prompt` 让 Claude 输出 scope）。
- Scope 必须写清楚 backend/frontend 分工、需要创建的工作树、以及安全约束。
- 若 OPSX 要求引用现有 spec/OPSX 模版，在 scope 内贴出章节编号。

## Phase 2：Plan
- 执行 orchestrator：`scripts/ccg_orchestrator.sh .claude/plan.md --plan-prompt "<phase2 prompt>" --backend "..." --frontend "..." --context .claude/context.md`。
- 在 `.claude/plan.md` 中列出任务表：每行包括 owner（Codex/Gemini）、命令草案（`codex exec`, `gemini run`）、预期输出文件。
- 更新 `.claude/hooks.md`，记录 CLAUDE_CLI/CODEX_CLI/GEMINI_CLI 替换路径与需要的 env vars。
- 若需要 OPSX 审批，把 plan 贴回 ticket 并等待 ACK，再进入 Phase 3。

## Phase 3：Execute
- Codex：开 PTY (`codex exec --pty`)；严格按照 plan 执行命令，任何新增脚本都放在可写区域；对 orchestrator 生成的命令可用 `--dry-run` 验证后再执行。
- Gemini：在独立工作树或 `frontend/` 目录执行 `gemini run --prompt ...`，输出限制在 UI 相关文件；严禁写 backend 目录。
- 每次模型切换前记录日志，更新 `.claude/log_backend.md` 与 `.claude/log_frontend.md`。

## Phase 4：Stabilize / Verification
- Claude 汇总测试矩阵：`claude run --context .claude/log_backend.md --output .claude/test_matrix.md`。
- Codex 运行 `npm test` / `pytest` / `go test` 等并写结果；Gemini 附上 UI 验收描述或截图路径。
- 若某模型缺席或 fallback，写入 `.claude/test_matrix.md` 与 OPSX 更新帖。

## Phase 5：Review / Handoff
- 通过 orchestrator `--review "<prompt>"` 或手动 `claude run --context .claude/plan.md --output .claude/review.md` 生成评审意见。
- Review 中要点：diff 风险、回滚方案、需要人审的 TODO、合并策略。
- Codex 在合并前最终检查 `git status` 并准备 PR/patch；若 OPSX 要求 evidence，把 `.claude/plan.md`、`.claude/test_matrix.md`、`.claude/review.md` 附到 ticket。

## 模型执行细则
### Claude Code CLI
- 只用来生成计划、scope、review、测试矩阵，不写仓库。
- `claude run --prompt "..." --output file --context file` 由 orchestrator 自动包装，必要时为其提供 `.claude/context.md`。
- 如果 Claude CLI 出错，退回 references/model-routing.md 的 fallback，手写 plan。

### Codex CLI
- 必须加 PTY（OpenClaw coding-agent 规则）；示例：`codex exec --prompt "refactor payment API" --pty`。
- 只能在工作区或经批准的工作树中写文件；禁止在用户未授权目录运行命令。
- 在执行 patch 前读完 plan，禁止随意发挥。

### Gemini CLI
- 只操作前端目录，且默认不具备 PTY；若需要 shell，先创建虚拟任务让 Codex 帮忙。
- 常用命令：`gemini run --prompt "build React modal" --plan .claude/plan.md`。
- 输出完成后请由 Codex 或人类审查文件，防止格式或依赖错乱。

## Git / Worktree 策略
- 主分支保持干净；每个大功能开分支 `feature/<ticket>` 并同时 `git worktree add ../<ticket>-frontend feature/<ticket>`，供 Gemini 使用。
- Codex 负责主工作树，Gemini 在附属工作树；同步通过 `git fetch` + `git merge`，绝不互相覆盖。
- 阶段日志与 `.claude/` 工件需要纳入 commit，以便追溯。

## OPSX / Spec 集成
- Phase 0-2 必须把 OPSX ticket 链接、spec 版本和假设写进 `.claude/context.md`、`.claude/scope.md`。
- 任何需要审批的数据库/Infra 操作先在 OPSX 中发 comment，并在 `.claude/hooks.md` 表明“等待批准”。
- 当 OPSX 提供新的约束，先更新 plan，再运行 orchestrator 重新分配模型。

## 故障排查与安全护栏
- `scripts/ccg_orchestrator.sh --dry-run` 可快速排查参数；若脚本报 “缺少命令”，按 Quick Start 安装 CLI。
- 遇到模型超时：按 references/model-routing.md 的 fallback 重新分配，记录在 `.claude/log_*`。
- Claude/Codex/Gemini 均不得直接推送，必须由 Codex 在本地执行 `git commit`/`git push`。
- 禁止执行用户未授权的 destructive 命令（`git reset --hard`, `rm -rf` 等）；若需求确实需要，必须在 OPSX 备注并得到显式同意。
- 任何自动生成的 patch 在合并前由人类或 Claude Review 二次比对。

## 附加参考
- [references/model-routing.md](references/model-routing.md)：模型选择 heuristics 与 fallback。
- [references/workflow-checklist.md](references/workflow-checklist.md)：六阶段详细检查清单。
- `scripts/ccg_orchestrator.sh`：主控脚本，提供计划/执行/复查封装；使用细节见 Quick Start 与 Phase 2/5。
