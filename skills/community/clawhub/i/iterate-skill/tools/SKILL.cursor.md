# iterate-skill for Cursor / Generic

Cursor 目前不原生支持 skill 注册，但可以通过 Agent 模式或自定义脚本实现 iterate 流程。本文件提供最小可运行实现思路。

---

## 方式一：Cursor Agent 模式 / Option 1: Cursor Agent Mode

1. 将本仓库的 `SKILL.md` 内容粘贴到 Cursor 的 Agent context 或自定义 system prompt 中。
2. 在项目根目录创建 `iterate.config.yaml`。
3. 在 Composer / Chat 中输入：

```text
/iterate "<goal>" [rounds] [no-limit]

# 示例
/iterate "提升代码质量" 10
/iterate "提升代码质量" no-limit
```

Cursor Agent 会按 SKILL.md 的流程执行：
- 读取配置
- 创建隔离分支
- 并行审查（通过多次 Agent 调用）
- 修复问题
- 运行验证命令
- merge/push（**opt-in**：`git.auto_merge` / `git.push_per_round` 默认 `false`，仅在用户显式开启时才自动合并并推送）

---

## 方式二：本地脚本驱动 / Option 2: Local Script Driver

如果你希望更可控，可写一个本地脚本协调 Cursor 的 Agent：

```bash
#!/usr/bin/env bash
# iterate.sh — 最小协调脚本示例

GOAL="$1"
ROUND="${2:-7}"
LIMIT_MODE="${3:-}"

if [ "$LIMIT_MODE" = "no-limit" ]; then
  ROUND=50
fi

git checkout -b "iterate/$(echo "$GOAL" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')-$(date +%s)"

for i in $(seq 1 "$ROUND"); do
  echo "=== Round $i ==="
  # 调用 Cursor CLI 或 Agent API 执行本轮 reviewer
  # cursor agent --prompt "..."
  # 人工 review 后决定是否继续
done
```

---

## 工具映射 / Tool Mapping

| iterate 概念 | Cursor / Generic | 说明 |
|--------------|------------------|------|
| 并行 reviewer | Agent 多次调用 / 脚本并行 | 每个维度或每个目录一个 Agent 调用 |
| 用户审批 | 对话确认 / 脚本暂停等待输入 | 架构修复必须经用户确认 |
| 文件编辑 | Agent 自动编辑 / 手动编辑 | 原子修复可由 Agent 直接改 |
| 架构修复子代理 | Agent 串行调用 | 一次只执行一个架构 task |
| 验证命令 | Terminal / Bash | 手动或脚本运行 |
| 配置校验 | 脚本调用 | `python scripts/validate.py config iterate.config.yaml` |

---

## Reviewer Prompt 模板 / Reviewer Prompt Template

```text
You are a {dimension} reviewer for the iterate skill.

Scope: {review.scope} (full = entire codebase, changed-only = files changed this round).
Focus: {focus from config/dimensions.yaml}.
Project context: {projectContext}.

DO NOT read .env, .env.*, *.key, secrets/, *.pem, *.p12, *.crt, *.cer, credentials.json, .aws/, .ssh/.

For each finding, report:
- file, line, severity, dimension, summary, failure_scenario, suggested_fix, is_atomic

EVIDENCE RULE: only report findings anchored in code you actually read —
fabricated paths or invented line numbers are EVIDENCE_VIOLATIONs.

Return strictly as JSON: { "findings": [...] }
If no findings, return { "findings": [] }.
```

---

## Meta-review 硬证据门禁 / Meta-review Evidence Gate

`reviewer.evidence_validation`（默认开启）：审查报告生成后需再审查一次，逐条校验每个 finding 的 `file`/`line` 是否真实存在于磁盘代码。伪造路径或越界行号以 `EVIDENCE_VIOLATION` 判 `needs_revision`。

`reviewer.coverage_validation`（默认开启）：将 reviewer 自报的 `readFiles` 与分配清单比对，明显缺口浮出 medium 的 `COVERAGE_GAP` 提示（不反转判定）。

---

## 纯审查模式 / review-only (dry-run)

当调用参数含 `review-only` 或 `dry-run`（如 `/iterate 审查代码 review-only`）时，**跳过 git 隔离、跳过所有修复与验证**，只执行只读审查循环并产出最终审查报告。此模式**绝不修改任何文件、绝不创建分支/worktree、绝不调用 fixer**。主模型必须校验参数后确认进入该模式，并在执行中拒绝一切写入动作。

收敛驱动：每轮把已知 findings 喂给 reviewer，迫使其只找新问题；某轮 0 新 findings 即收敛停止。产出三级报告：审查报告 → meta-review（`COUNT_MATCH`/`SEVERITY_SUM`/`DIMENSION_SUM`/`SORT_ORDER`/`CONVERGENCE`/`ROUND_SHAPE`）→ 最终审查报告（`approved` / `needs_revision`）。硬证据门禁（`reviewer.evidence_validation`，默认开启）会逐条校验 finding 的 `file`/`line`，伪造或越界即 `EVIDENCE_VIOLATION` 翻转为 `needs_revision`。详见主 `SKILL.md`。

**Cursor 实现要点**：全部 reviewer 用 Agent 只读启动；不执行任何编辑/运行验证命令；不调用 `git checkout -b`。若脚本误触发写入，主模型应立即拒绝并以只读方式继续。

---

## Onboarding / Personalization

首次调用 `/iterate` 前需先完成 onboarding：生成 `ITERATE.md` 知识库与项目级 `iterate.config.yaml`（含 `onboarding.fingerprints` 漂移指纹）。可在终端运行 `iterate onboard` 交互式完成，或由 AI 通道自动扫描。项目专属约束（禁区、风险区、已知意图等）通过 `iterate personalize` 追加。详见主 `SKILL.md`。

---

## 安全提醒 / Safety Reminder

- 运行时只执行 `validation.commands.<module>` 中显式配置的精确命令，不自行拼装、不基于前缀构造命令；不在其中的命令直接拒绝，不可通过用户确认绕过。未配置命令的模块跳过。`validation.command_whitelist` 仅为配置期校验辅助字段，无运行时约束力。
- 绝不 force-push。
- 绝不直接在 main/master 上提交。
- merge/push 默认关闭（`git.auto_merge` / `git.push_per_round = false`）；如需合并推送，先确认当前仓库与远程，再人工 review 后执行。
