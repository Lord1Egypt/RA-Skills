# iterate-skill for Trae

Trae 实现 iterate skill 的核心要点：用 `Task` 启动并行 reviewer，用 `AskUserQuestion` 做用户审批，用 `RunCommand` 跑验证命令。

---

## 目录放置 / Placement

```text
~/.trae/skills/iterate/SKILL.md
# 或项目内
<project>/.trae/skills/iterate/SKILL.md
```

将本仓库的 `SKILL.md` 复制到上述位置即可。

---

## 触发方式 / Invocation

在 Trae 对话中输入（参数通过 Agent Skills 占位符 `$0` / `$1` / `$2` 注入）：

```text
/iterate "<goal>" [rounds] [no-limit]

# 示例
/iterate "提升代码质量" 10
/iterate "提升代码质量" no-limit
```

---

## 工具映射 / Tool Mapping

| iterate 概念 | Trae 工具 | 说明 |
|--------------|-----------|------|
| 并行 reviewer | `Task` × N | `subagent_type: "search"` 用于代码审查；`subagent_type: "general_purpose_task"` 用于汇总 |
| 按目录拆分 reviewer | `Task` per directory | 大项目时，每个子任务审查一个目录 |
| 用户审批 | `AskUserQuestion` | 呈现架构修复列表，等待用户选择 |
| 文件编辑 | `Read` / `Edit` / `Write` | 原子修复由主模型直接操作 |
| 架构修复子代理 | `Task` (serial) | 每个 task 串行执行，完成后才启动下一个 |
| 验证命令 | `RunCommand` | 执行 `validation.commands` 中的命令 |
| 配置校验 | `RunCommand` | `python scripts/validate.py config iterate.config.yaml` |

---

## Reviewer Task 示例 / Reviewer Task Example

```text
subagent_type: "search"
description: "security reviewer"
query: |
  Review the codebase for security issues ONLY.

  Scope: {review.scope}
  Focus: injection, path traversal, hardcoded secrets, input validation.
  Project context: {projectContext}

  Do NOT read .env, .env.*, *.key, secrets/, *.pem, *.p12, *.crt, *.cer, credentials.json, .aws/, .ssh/.

  For each finding report: file, line, severity, dimension, summary,
  failure_scenario, suggested_fix, is_atomic.

  EVIDENCE RULE: only report findings anchored in code you actually read.
  Fabricated paths or invented line numbers are EVIDENCE_VIOLATIONs.

  Return strictly as JSON: { "findings": [...] }
```

---

## Meta-review 硬证据门禁 / Meta-review Evidence Gate

`reviewer.evidence_validation`（默认开启）要求审查报告本身再被审查：逐条校验每个 finding 的 `file`/`line` 是否真实存在于磁盘代码中。任何伪造路径或越界行号都会以 `EVIDENCE_VIOLATION` 判 `needs_revision`。

`reviewer.coverage_validation`（默认开启）将 reviewer 自报的 `readFiles` 与分配清单比对，明显缺口浮出 medium 的 `COVERAGE_GAP` 提示（不反转判定）。

---

## 纯审查模式 / review-only (dry-run)

当调用参数含 `review-only` 或 `dry-run`（如 `/iterate 审查代码 review-only`）时，**跳过 git 隔离、跳过所有修复与验证**，只执行只读审查循环并产出最终审查报告。此模式**绝不修改任何文件、绝不创建分支/worktree、绝不调用 fixer**。主模型必须校验参数后确认进入该模式，并在执行中拒绝一切写入动作。

收敛驱动：每轮把已知 findings 喂给 reviewer，迫使其只找新问题；某轮 0 新 findings 即收敛停止。产出三级报告：审查报告 → meta-review（`COUNT_MATCH`/`SEVERITY_SUM`/`DIMENSION_SUM`/`SORT_ORDER`/`CONVERGENCE`/`ROUND_SHAPE`）→ 最终审查报告（`approved` / `needs_revision`）。硬证据门禁（`reviewer.evidence_validation`，默认开启）会逐条校验 finding 的 `file`/`line`，伪造或越界即 `EVIDENCE_VIOLATION` 翻转为 `needs_revision`。详见主 `SKILL.md`。

**Trae 实现要点**：全部 reviewer 用 `Task` 只读启动；不执行任何 `Edit`/`Write`/`RunCommand`（验证）；不调用 `git checkout -b`。若脚手架误触发写入，主模型应立即拒绝并以只读方式继续。

---

## Onboarding / Personalization

首次调用 `/iterate` 前需先完成 onboarding：生成 `ITERATE.md` 知识库与项目级 `iterate.config.yaml`（含 `onboarding.fingerprints` 漂移指纹）。可在 Trae 终端运行 `iterate onboard` 交互式完成，或由 AI 通道自动扫描。项目专属约束（禁区、风险区、已知意图等）通过 `iterate personalize` 追加。详见主 `SKILL.md`。

---

## 子代理失败处理 / Sub-agent Failure

子代理返回失败时，主模型必须：

1. 记录失败原因到 `.iterate_decisions.md`。
2. 使用 `AskUserQuestion` 询问用户：
   - 继续（continue）
   - 跳过该 task（skip）
   - 中止本轮（abort round）

---

## 验证命令执行前检查 / Pre-validation Check

运行 `RunCommand` 前：只执行 `validation.commands.<module>` 中**显式配置的精确命令**，不自行拼装、不基于前缀构造命令；未配置命令的模块跳过。

1. 确认要执行的命令正好是 `validation.commands` 中某条精确命令（不在其中的命令直接拒绝，不可通过用户确认绕过）。
2. 执行命令并捕获输出。

`validation.command_whitelist` 仅为配置期校验辅助字段（`scripts/validate.py`），可缺省、无运行时约束力，运行时以 `validation.commands` 为唯一权威白名单。
