# iterate-skill for Claude Code

Claude Code 实现 iterate skill 的核心要点：用 `/workflow` 或 `/agent` 启动并行 reviewer，用 Plan/Approve 模式做用户审批，用 `Bash` 工具跑验证命令。

---

## 目录放置 / Placement

```text
~/.claude/skills/iterate/SKILL.md
# 或项目内
<project>/.claude/skills/iterate/SKILL.md
```

将本仓库的 `SKILL.md` 复制到上述位置即可。

---

## 触发方式 / Invocation

在 Claude Code 中输入（参数通过 `$ARGUMENTS` / `$0` / `$1` / `$2` 注入）：

```text
/iterate "<goal>" [rounds] [no-limit]

# 示例
/iterate "提升代码质量" 10
/iterate "提升代码质量" no-limit
```

参数通过 Agent Skills 标准占位符 `$0` / `$1` / `$2` 注入，也可使用 `$goal` / `$rounds` / `$limit_mode`。

> 注意：本 skill 需要由用户显式调用 `/iterate` 才会触发。

---

## 工具映射 / Tool Mapping

| iterate 概念 | Claude Code 工具 | 说明 |
|--------------|------------------|------|
| 并行 reviewer | `Workflow` / `Agent` × N | 每个 reviewer 一个 agent，并行执行 |
| 按目录拆分 reviewer | `Agent` per directory | 大项目时按目录分组 |
| 用户审批 | `EnterPlanMode` / `ExitPlanMode` | 架构修复进入 Plan 模式，用户 approve 后执行 |
| 文件编辑 | `Read` / `Edit` / `Write` | 原子修复由主模型直接操作 |
| 架构修复子代理 | `Agent` (serial) | 串行委派，每个完成后再启动下一个 |
| 验证命令 | `Bash` | 执行 `validation.commands` 中的命令 |
| 配置校验 | `Bash` | `python scripts/validate.py config iterate.config.yaml` |

---

## Workflow JSON 示例 / Workflow JSON Example

```json
{
  "name": "iterate-security-review",
  "description": "Run security dimension reviewer",
  "steps": [
    {
      "tool": "Read",
      "path": "iterate.config.yaml"
    },
    {
      "tool": "Read",
      "path": "CLAUDE.md",
      "if_exists": true
    },
    {
      "tool": "Agent",
      "prompt": "Review the codebase for security issues ONLY. Scope: {review.scope}. Focus: injection, path traversal, hardcoded secrets, input validation. Project context: {projectContext}. Do NOT read .env, .env.*, *.key, secrets/, *.pem, *.p12, *.crt, *.cer, credentials.json, .aws/, .ssh/. EVIDENCE RULE: only report findings anchored in code you actually read — fabricated paths or invented line numbers are EVIDENCE_VIOLATIONs. Return strictly as JSON with 'findings' array."
    }
  ]
}
```

---

## Meta-review 硬证据门禁 / Meta-review Evidence Gate

`reviewer.evidence_validation`（默认开启）：审查报告生成后需再审查一次，逐条校验每个 finding 的 `file`/`line` 是否真实存在于磁盘代码。伪造路径或越界行号以 `EVIDENCE_VIOLATION` 判 `needs_revision`。

`reviewer.coverage_validation`（默认开启）：将 reviewer 自报的 `readFiles` 与分配清单比对，明显缺口浮出 medium 的 `COVERAGE_GAP` 提示（不反转判定）。

---

## 纯审查模式 / review-only (dry-run)

当调用参数含 `review-only` 或 `dry-run`（如 `/iterate 审查代码 review-only`）时，**跳过 git 隔离、跳过所有修复与验证**，只执行只读审查循环并产出最终审查报告。此模式**绝不修改任何文件、绝不创建分支/worktree、绝不调用 fixer**。主模型必须校验参数后确认进入该模式，并在执行中拒绝一切写入动作。

收敛驱动：每轮把已知 findings 喂给 reviewer，迫使其只找新问题；某轮 0 新 findings 即收敛停止。产出三级报告：审查报告 → meta-review（`COUNT_MATCH`/`SEVERITY_SUM`/`DIMENSION_SUM`/`SORT_ORDER`/`CONVERGENCE`/`ROUND_SHAPE`）→ 最终审查报告（`approved` / `needs_revision`）。硬证据门禁（`reviewer.evidence_validation`，默认开启）会逐条校验 finding 的 `file`/`line`，伪造或越界即 `EVIDENCE_VIOLATION` 翻转为 `needs_revision`。详见主 `SKILL.md`。

**Claude Code 实现要点**：全部 reviewer 用 `Agent`/`Workflow` 只读启动；不执行任何 `Edit`/`Write`/`Bash`（验证）；不调用 `git checkout -b`。若脚手架误触发写入，主模型应立即拒绝并以只读方式继续。

---

## Onboarding / Personalization

首次调用 `/iterate` 前需先完成 onboarding：生成 `ITERATE.md` 知识库与项目级 `iterate.config.yaml`（含 `onboarding.fingerprints` 漂移指纹）。可在终端运行 `iterate onboard` 交互式完成，或由 AI 通道自动扫描。项目专属约束（禁区、风险区、已知意图等）通过 `iterate personalize` 追加。详见主 `SKILL.md`。

---

## 子代理失败处理 / Sub-agent Failure

子代理返回失败时：

1. 记录到 `.iterate_decisions.md`。
2. 提示用户并等待明确指令（continue / skip / abort）。

---

## 验证命令安全 / Validation Safety

运行时只执行 `validation.commands.<module>` 中**显式配置的精确命令**，不自行拼装、不基于前缀构造命令。未配置命令的模块跳过。

`validation.command_whitelist` 仅为配置期校验辅助字段（`scripts/validate.py`），可缺省、无运行时约束力——即便未配置，运行时仍以 `validation.commands` 为唯一权威白名单。不在其中的命令**直接拒绝，不可通过用户确认绕过**（与个性化硬白名单一致）。
