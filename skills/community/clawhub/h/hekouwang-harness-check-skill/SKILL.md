---
name: hekouwang-harness-check-skill
license: MIT
description: "体检会勇禾口王内容工作流 Harness：跑 verify.sh 及治理、Hook、安全门、Episode 检查"
metadata:
  slug: hekouwang-harness-check-skill
  display_name: hekouwang Harness Check
  version: 1.0.1
  summary: 证据驱动的 Agent Harness 独立验收器：检查本地、暂存区、CI、Hook、治理契约和真实宿主边界。
  tags: harness, agent, governance, verification, audit
  homepage: https://huiyonghkw.github.io/hekouwang-harness-check-skill/
  openclaw:
    homepage: https://huiyonghkw.github.io/hekouwang-harness-check-skill/
    requires:
      bins:
        - bash
        - python3
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# 会勇禾口王 Harness 检查器

## 目标

把 Harness 检查变成可重复、可审计的交付动作。检查逻辑以仓库 `.harness/` 为唯一真源；本 Skill 负责选择入口、完整执行、解释结果和暴露未覆盖边界，不复制或改写检查规则。

## 信任边界（运行前必过）

本 Skill 不自带校验代码，执行的是**目标仓库自己的** `.harness/` 脚本，它们以当前用户权限运行；`--working-tree` / `--local` 模式按设计会读取本机 Skill 目录与 Agent Memory，并可能写入脱敏的观测事件。

- 只在用户自己的、或用户明确表示信任的仓库里跑 `--working-tree`、`--staged`、`--local`。
- 来源不明或第三方仓库：先告知上述影响并征得同意；默认改跑 `--ci-hermetic`（不依赖本机 Skill/Memory），且先通读将要执行的 `.harness/scripts/verify.sh`。
- 不为检查去读取 `.env`、密钥或凭据文件。

## 入口选择

先定位仓库根目录：必须能找到 `.harness/scripts/verify.sh`。所有命令从仓库根目录运行。

| 用户目的 | 入口 |
| --- | --- |
| 检查当前本地工作区 | `bash .harness/scripts/verify.sh --working-tree` |
| 检查准备提交的治理改动 | `bash .harness/scripts/verify.sh --staged` |
| 本机 CI 契约/fixture 回归 | `bash .harness/scripts/verify.sh --ci` |
| 复现远端 CI、排除本机 Skill/宿主软链 | `bash .harness/scripts/verify.sh --ci-hermetic` |
| 只诊断结构、链接和治理契约 | `bash .harness/scripts/harness-check.sh --local` 或 `--ci` |

不要默认只跑 `harness-check.sh` 就宣称 Harness 完成；完整验收应优先使用 `verify.sh`。

## 执行规则

1. 直接运行命令并保留退出码。不要用 `| head`、`|| true` 或吞掉 stderr 的方式判断成功。
2. 需要保存长日志时写入临时目录，完整读取失败段；不要把临时日志当成任务证据提交。
3. 先报告自动化结果，再报告人工检查；两者不能合并成一个“全部通过”。
4. 从实际输出读取检查数量。`--ci` 是本机 fixture 回归，只有 `--ci-hermetic` 才能证明干净 clone 的 CI 入口可复现。基础闭环曾输出本地 `722`、CI `165` 项；这些都不是永久硬编码的总分；数量变化时如实记录，不自行补算或夸大。
5. `⚠️` 是警告，不等于 `✅`；只要任一应通过检查返回非零，就判定自动检查失败。
6. 检查失败时先指出失败命令、失败项目和可复现路径。只有用户明确要求修复时才改文件；改前遵守 `AGENTS.md` 的范围说明和确认规则。
7. 不使用 `--no-verify` 绕过 Hook，不为让检查通过而修改计数、删除反例、关闭治理项或把宿主烟测写成自动化证据。

## 结果报告格式

至少输出以下五部分：

1. **模式与范围**：`working-tree`、`staged`、`ci` 或 `ci-hermetic`，以及检查到的仓库/提交。
2. **自动化结论**：命令退出状态；列出通过、失败和警告。若输出包含 Runtime Governance 数量，注明是本地还是 CI。
3. **失败定位**：保留原始检查标签和复现命令，不把“工具没输出”解释成通过。
4. **人工/宿主边界**：说明是否实际触发了 Claude Code、Cursor、CodeBuddy、Codex 的 Hook；是否检查了真实平台视觉、浏览器或 MCP 外部副作用。
5. **下一步**：修复、补宿主烟测、记录失败台账，或明确“自动化通过但不能交付”的原因。

## 不能替代的人工检查

语义 Hook 配置校验和 fixture 正反例只能证明配置可解析、规则可归一化、失败路径能被拦截，不能证明真实宿主一定触发。以下情况必须单独标记为“宿主烟测待补”：

- 在四个真实 Agent 宿主中触发一次允许、询问和阻断路径；
- 在真实编辑器、浏览器、公众号/头条/小红书宿主中检查最终呈现；
- 检查文章事实、来源、自然度和视觉质量；
- 检查 MCP 工具的真实外部副作用和人工确认链路。

## 失败后的最小动作

- `verify.sh` 失败：按输出先运行对应的单项测试，例如 `bash .harness/tests/test-hook-config.sh`。
- 适配链接失败：先查看 `bash .harness/scripts/sync-agent-adapters.sh --check`；未经用户明确要求，不自动使用 `--fix`。
- Runtime Governance 漂移：检查 `.harness/contracts/`、`AGENTS.md`、`.agents/skills/` 和 Memory 真源，不直接改测试让它变绿。
- 内容任务预检：同时加载 `hekouwang-precheck`，并把自动检查和人工视觉检查分开报告。

详细命令、检查层级和历史基线/当前数量口径见 [`references/check-matrix.md`](references/check-matrix.md)。面向维护者的开源说明和流程图见 [`README.md`](README.md)。
