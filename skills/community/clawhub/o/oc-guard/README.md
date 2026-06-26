# oc-guard-skill

<p align="center">
  <img src="docs/readme_logo.png" alt="oc-guard mascot with security shield" width="960" />
</p>

## 公告 | Announcement

`oc-guard-skill` 已正式发布到 GitHub 与 ClawHub。  
This project is now publicly available on GitHub and ClawHub.

- 目标：防止 OpenClaw 配置被误改导致服务中断。  
  Goal: prevent OpenClaw outages caused by unsafe config edits.
- 机制：先 `plan`，后 `apply --confirm`，失败自动回滚。  
  Workflow: `plan` first, then `apply --confirm`, with automatic rollback on failure.

## 目录 | Table of Contents

- [简介 | Overview](#简介--overview)
- [工作流图 | Workflow Diagram](#工作流图--workflow-diagram)
- [功能 | Features](#功能--features)
- [包含文件 | Included Files](#包含文件--included-files)
- [不包含 | Not Included](#不包含--not-included)
- [前置依赖 | Prerequisites](#前置依赖--prerequisites)
- [安装 | Install](#安装--install)
- [环境变量覆盖 | Environment Overrides](#环境变量覆盖--environment-overrides)
- [使用方法 | Usage](#使用方法--usage)
- [输出协议 | Output Contract](#输出协议--output-contract)
- [发布后验收 | Post-publish Verification](#发布后验收--post-publish-verification)
- [安全说明 | Security Notes](#安全说明--security-notes)
- [标签与发布 | Tags and Releases](#标签与发布--tags-and-releases)
- [许可证 | License](#许可证--license)

## 简介 | Overview

OpenClaw 配置安全守卫工具。  
Safe config guard for OpenClaw.

- 用 `plan` 预览变更和风险。 / Use `plan` to preview changes and risk.
- 用 `apply --confirm` 执行高风险变更。 / Use `apply --confirm` for high-risk changes.
- 内置备份与回滚。 / Built-in backup and rollback.
- 输出中英并行执行回执。 / Bilingual execution receipts.

## 工作流图 | Workflow Diagram

<p align="center">
  <img src="docs/workflow.png" alt="oc-guard safe config workflow diagram" width="960" />
</p>

## 功能 | Features

- 自然语言转受控提案（`plan`） / Natural language to guarded proposal (`plan`)
- 高风险确认门槛（`apply --confirm`） / High-risk confirmation gate
- 校验渠道、绑定、agent、模型引用 / Validate channels, bindings, agents, model references
- 关键枚举值校验（如 `tools.exec.ask`） / Enum guardrails for risky fields (e.g. `tools.exec.ask`)
- 官方 `openclaw config validate` 二次校验 / Secondary validation via `openclaw config validate`
- 全局与 agent 本地模型配置漂移检查 / Drift detection between global and agent-local model configs
- 应用前自动备份 / Auto backup before apply
- 应用后 canary（main/bro）可用性探测 / Post-apply canary checks (main/bro)
- 失败自动回滚 / Auto rollback on failure
- 12位验签码执行回执 / 12-char signed execution receipt

## 包含文件 | Included Files

- `SKILL.md`
- `scripts/oc-guard`
- `scripts/oc-guard.py`
- `templates/proposal.template.json`
- `docs/SAFETY.md`
- `CHANGELOG.md`

## 不包含 | Not Included

- 个人配置文件（如 `~/.openclaw/openclaw.json`） / Personal config files
- 日志、备份、运行产物 / Logs, backups, runtime artifacts
- `apiKey`、`token`、`appSecret` 等敏感信息 / Secrets (`apiKey`, `token`, `appSecret`)

## 前置依赖 | Prerequisites

- Python 3.9+
- OpenClaw CLI
- OpenCode CLI

## 安装 | Install

```bash
chmod +x scripts/oc-guard
mkdir -p ~/.local/bin
ln -sf "$PWD/scripts/oc-guard" ~/.local/bin/oc-guard
```

## 环境变量覆盖 | Environment Overrides

支持以下可选环境变量：  
Optional environment variables:

- `OPENCLAW_HOME`
- `OCGUARD_CONFIG_PATH`
- `OCGUARD_BACKUP_DIR`
- `OCGUARD_OPENCLAW_BIN`
- `OCGUARD_OPENCODE_BIN`
- `OCGUARD_RECEIPT_SECRET`
- `OCGUARD_RECEIPT_SECRET_FILE`

## 使用方法 | Usage

```bash
oc-guard plan "add a new feishu bot and bind it to github agent"
oc-guard apply --confirm "add a new feishu bot and bind it to github agent"
```

或使用提案文件：  
Or with a proposal file:

```bash
oc-guard plan --proposal /tmp/openclaw-config-proposal.json
oc-guard apply --confirm --proposal /tmp/openclaw-config-proposal.json
```

## 输出协议 | Output Contract

每条命令都会返回：  
Every command returns:

- `【执行回执 | Execution Receipt】`
- `执行来源/操作类型/请求编号/执行状态/12位验签码`  
  `executor/operation/request id/status/12-char signature`
- `【本次内容 | Details】`

未执行时必须返回：  
If not executed, must return:

- `【模型说明-未执行】`

`plan` 失败时可查看：`/tmp/oc-guard-last-opencode-output.txt`（仅用于本机诊断）。  
If `plan` fails, inspect `/tmp/oc-guard-last-opencode-output.txt` for local diagnostics.

## 发布后验收 | Post-publish Verification

每次发布到 ClawHub 后，至少执行以下检查：
After each ClawHub publish, run at least the checks below:

```bash
clawhub inspect oc-guard-skill --files
clawhub inspect oc-guard-skill --file SKILL.md
```

- `--files` 输出中必须包含 `scripts/oc-guard.py`
- `SKILL.md` frontmatter 必须包含 `metadata.openclaw.requires`（声明所需二进制/环境）

## 标签与发布 | Tags and Releases

- Git 标签遵循语义化版本：`vMAJOR.MINOR.PATCH`
- 发布顺序：更新 `CHANGELOG.md` -> 创建 tag -> 创建 GitHub Release -> 校验 ClawHub 包内容
- 每次发布都应附带可核验信息：
  - 关键变更摘要（why > what）
  - 受影响文件路径
  - 本地验证命令与结果
  - ClawHub `inspect --files` 验收结果

## 安全说明 | Security Notes

请勿公开以下目录中的真实内容：  
Do not publish real contents from:

- `~/.openclaw/**`
- `/tmp/openclaw*`
- `/tmp/oc-guard-*`

可以公开“路径说明”和“文件名”，不要公开真实配置与日志内容。  
Path references and file names are okay; real config/log contents are not.

若 `oc-guard` 返回失败或阻断，禁止绕过 guard 直接修改配置文件。  
If `oc-guard` returns failed/blocked, do not bypass guard by editing config directly.

## 许可证 | License

MIT
