---
name: pipl-audit
description: |
  PIPL Audit — 个人信息保护法合规深度审计（基于《个人信息保护法》PIPL 2021-11-01 施行
  及配套规则），覆盖 9 大审计域 32 项审计检查（审计范围/告知同意/处理原则/敏感信息与未成年人/
  个人权利/自动化决策/跨境传输/数据安全与事件响应/治理与持续合规）。免费安装；
  评分运行于 CQDev 云端合规引擎。无 Key 时自动匿名试用（5 次真实云端评分 / 7 天窗口），
  额度用尽后引导注册。
  Use when: the user explicitly asks to run the pipl-audit skill (e.g. "run pipl-audit",
  "use the pipl-audit skill", "做 PIPL 深度审计"). Do NOT activate on generic mentions of
  "PIPL" or "个保法" — this skill transmits answers to a third-party cloud and must be
  opted into explicitly by name.
  Trigger (explicit opt-in only): pipl-audit, run pipl-audit, use pipl-audit skill, PIPL 深度审计, PIPL 合规审计
  Pricing: Free skill; cloud scoring uses points (Check 1 / Audit 10 per run) from compliancehub.cn
  ⚠️ Cloud scoring sends your 32 answers to compliancehub.cn; use --non-interactive for a fully offline preview that never contacts the cloud. Without a Key the skill runs an anonymous trial (up to 5 scored runs) using a local random anon_id; registering gives a free Key with 100 calls.
  🔐 API Key: get a free API Key (100 free calls) at compliancehub.cn/account.html (register in the browser; the Key is shown instantly). Provide it via the COMPLIANCEHUB_API_KEY environment variable, or save it to ~/.config/compliancehub/pipl-audit.key (mode 0600). Registration is done on the website — the terminal no longer collects credentials.
  💡 Free preview: --non-interactive lists the 32 audit items without a Key
  Locale: zh-CN（交互默认中文，英文可按需提供）（交互与提示以中文为主，法律条款名称保留中文原文以确保准确）。
permissions:
  network:
    - "https://compliancehub.cn"
  filesystem:
    write:
      - "~/.config/compliancehub"
  env:
    - "COMPLIANCEHUB_API_KEY"
---

# 🔒 PIPL Audit — 个人信息保护法合规深度审计（免费 · 云端评分）

## Overview
PIPL Audit 是面向处理中国境内自然人个人信息主体的**免费**合规深度审计（云端评分），
覆盖 9 大审计域 32 项审计检查：告知同意、处理原则、数据安全、敏感个人信息、个人权利、
自动化决策、跨境传输、合规治理。评分运行于 CQDev 云端合规引擎。

## How it works (free + cloud)
> ⚠️ **Your answers leave this machine.** When you run a *scored* check, your responses to the
> 32 audit questions are transmitted to the CQDev cloud at `compliancehub.cn`
> for scoring. Those answers can cover sensitive details — consumer-data practices, service
> providers, security controls, and legal exposure. Only proceed if you are comfortable sending
> them to `compliancehub.cn`. Run `--non-interactive` for a fully **offline** preview that never
> contacts the cloud.

- The skill is free to install.
- Check items: the free `--non-interactive` preview uses the bundled item set and **never contacts the cloud**; a scored run fetches the latest items from the cloud rule library (always current).
- Scoring + quota are computed in the cloud; you get a professional report locally.
- Scoring: no Key? The anonymous trial (5 real cloud-scored runs) runs automatically. Register for a free API Key (100 calls) to keep going.

## What it checks (32 items)
| # | Check | Authority |
|---|-------|-----------|
| 1 | 审计范围与制度基础 | 第 6-9 条 / 第 51 条 |
| 2 | 数据资产清单 | 第 6 条 / 第 51 条 |
| 3 | 人员培训与考核 | 第 9 条 / 第 52 条 |
| 4 | 告知内容完整性 | 第 13-14 条 |
| 5 | 同意有效性 | 第 13-15 条 / 第 29 条 |
| 6 | 撤回机制 | 第 15-16 条 |
| 7 | 同意留痕 | 第 16 条 |
| 8 | 最小必要审查 | 第 6 条 |
| 9 | 公开透明 | 第 7 条 |
| 10 | 数据质量 | 第 8 条 |
| 11 | 敏感信息识别 | 第 28 条 |
| 12 | 敏感处理独立同意 | 第 29 条 |
| 13 | 未成年人保护 | 第 31 条 |
| 14 | 权利受理渠道 | 第 44-45 条 |
| 15 | 权利响应流程 | 第 44-48 条 |
| 16 | 删除权执行 | 第 47 条 |
| 17 | 可携带权 | 第 45 条第 3 款 |
| 18 | 解释与人工干预 | 第 24 条 / 第 48 条 |
| 19 | 自动化决策告知 | 第 24 条 |
| 20 | 公平性审计 | 第 24 条 |
| 21 | 出境路径合规 | 第 38 条 |
| 22 | 出境告知与单独同意 | 第 39 条 |
| 23 | 出境再评估 | 第 38-40 条 |
| 24 | 安全技术措施 | 第 9 条 / 第 51 条 |
| 25 | 安全管理组织 | 第 51 条 |
| 26 | 事件监测与分级 | 第 57 条 |
| 27 | 事件响应与通知 | 第 57 条 |
| 28 | 个人信息保护负责人 | 第 52 条 |
| 29 | 保护影响评估 | 第 55-56 条 |
| 30 | 定期合规审计 | 第 54 条 |
| 31 | 委托处理管理 | 第 21-23 条 |
| 32 | 大型平台特别义务 | 第 58 条 |

## Usage

### Free preview (no Key)
```bash
python3 scripts/pipl-audit.py --non-interactive
```
### Anonymous trial (no Key)
Just run the full check — without a Key the skill issues a local random anon_id and scores in the cloud
(5 free runs / 7-day window). When the trial runs out it prints the one-click registration page,
carrying your anon_id so the trial progress carries over after registering.

### Get a free API Key
1. Open https://compliancehub.cn/account.html?skill=pipl-audit in your browser and register (the Key is shown instantly after registration).
2. Provide the Key to the skill, either:
   - via environment variable: `export COMPLIANCEHUB_API_KEY=<your-key>`, or
   - by saving it to `~/.config/compliancehub/pipl-audit.key` (mode 0600).
Then run the check below; no terminal login is needed.

### Full check + report
```bash
python3 scripts/pipl-audit.py --format html -o pipl-report.html
```
逐项完成 32 项审计；云端评分并返回 HTML 审计报告（含风险等级与整改建议）。

## Agent guide
When a user asks for a PIPL compliance audit:
1. Run `--non-interactive` to preview the 32 items (no Key needed).
2. Run the full check. Without a Key it automatically uses the anonymous trial (5 real cloud-scored runs) — the user gets the complete report immediately. When the trial runs out the skill prints the one-click registration page (with the trial's anon_id), and after registering the same run continues under their free API Key (100 calls).

## Security & data handling
- **No terminal credentials:** The skill never collects your email or password. Registration and Key issuance happen on the website (compliancehub.cn/account.html); the skill only consumes the resulting API Key. This removes any credential-handling path from the CLI.
- **Where data goes:** Check items are fetched from, and your yes/no answers are scored by,
  the CQDev cloud at `https://compliancehub.cn` (the operator's official endpoint,
  pinned in code and **not** overridable by environment variable). Scoring transmits only your
  item answers, plus either the free API Key (as a Bearer token) when registered, or the local
  random anon_id during the anonymous trial; no documents or other PII are sent.
- **Anonymous trial id:** A local random `anon_id` (`~/.config/compliancehub/pipl-audit.anon_id`,
  0600, carries no personal data) persists only to continue the anonymous trial; your answers
  are never stored locally.
- **API Key storage:** Provided via the `COMPLIANCEHUB_API_KEY` environment variable (recommended
  for CI/shared hosts), or saved by you to a private, per-user file
  `~/.config/compliancehub/pipl-audit.key` with `0600` permissions — **outside** this skill
  folder, so it is never committed to source control or shared with the workspace.
- **No shell execution:** This skill runs as a Python 3 subprocess using only the standard
  library (`urllib`, `json`, `ssl`, `getpass`). It does **not** spawn a shell, does not run
  arbitrary OS commands, and does not execute external binaries.
- **Not a rogue/autonomous agent:** Writing the Key to `~/.config/compliancehub/` is ordinary
  API-key persistence for your convenience — not agent installation, not auto-start, and not
  self-modification. The skill does nothing unless you invoke it from the terminal.
- **Preview without cloud:** `--non-interactive` lists the 32 items and never contacts the cloud.
- Always confirm the destination is `compliancehub.cn` before running a scored check.

## Legal disclaimer
This tool provides general compliance guidance only and is **not legal advice**.
Consult qualified counsel for formal opinions. Laws change; verify against official sources.

## License
MIT.
