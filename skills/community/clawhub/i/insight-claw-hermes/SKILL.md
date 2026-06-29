---
name: insight-claw-hermes
description: Download, configure, run, verify, and troubleshoot Insight Claw, an A-share self-selected stock analysis pipeline.
version: 0.3.1
author: GeraltJc
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [Finance, A-Share, CLI, Analysis, Automation]
    related_skills: []
    config:
      - key: insight-claw.repo_dir
        description: Local directory where the Insight Claw repository should be cloned or reused.
        default: "~/insight-claw"
        prompt: Insight Claw repository directory
      - key: insight-claw.default_stocks
        description: Default self-selected stocks for first validation runs.
        default: "000001,600519"
        prompt: Default stock codes for Insight Claw validation
required_environment_variables:
  - name: AIHUBMIX_KEY
    prompt: AIHubMix API key
    help: Configure this when using the recommended OpenAI-compatible AIHubMix path.
    required_for: LLM structured analysis
  - name: OPENAI_API_KEY
    prompt: OpenAI-compatible API key
    help: Configure this as the primary key or as fallback when AIHUBMIX_KEY is not available.
    required_for: LLM structured analysis
---
# Insight Claw

Insight Claw 是面向 A 股自选股的自动化自选股分析流水线。它围绕一组自选股收集行情数据、筹码分布和搜索情报，调用模型生成结构化分析，最终产出可保存或推送的决策结果。

## When to Use

Use this skill when a user wants Hermes Agent to download, configure, run, verify, or troubleshoot Insight Claw.

## Quick Reference

Insight Claw is an A-share self-selected stock analysis pipeline.

For expanded commands, environment examples, GitHub Actions setup, and troubleshooting details, read:

- `references/quickstart.md`
- `references/troubleshooting.md`

| Task | Command |
| --- | --- |
| Download | `git clone https://github.com/GeraltJc/insight-claw.git insight-claw` |
| Create environment | `python -m venv .venv` |
| Install dependencies | Download-probe default PyPI and the Tsinghua mirror, then install with the faster successful index for this run only. |
| First validation | `.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify` |

If the user is already inside an Insight Claw checkout, reuse it instead of cloning a duplicate repository.

## Execution Contract

Hermes should not clone and reinstall on every request. Use this decision flow:

### First-time setup

Run this setup flow only when the Insight Claw repository or `.venv` environment is missing:

```bash
git clone https://github.com/GeraltJc/insight-claw.git insight-claw
cd insight-claw
python -m venv .venv
.venv/bin/python -m pip download --no-cache-dir --no-deps --dest /tmp/insight-claw-pip-probe-pypi --index-url https://pypi.org/simple requests==2.32.5
.venv/bin/python -m pip download --no-cache-dir --no-deps --dest /tmp/insight-claw-pip-probe-tuna --index-url https://pypi.tuna.tsinghua.edu.cn/simple requests==2.32.5
```

Then run exactly one dependency install command: default PyPI if it is faster, or the Tsinghua mirror if it is faster/default PyPI fails. After dependencies are installed, run the first validation:

```bash
.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Before installing dependencies, always compare default PyPI and the Tsinghua mirror with an actual package download probe, not only index metadata:

```bash
.venv/bin/python -m pip download --no-cache-dir --no-deps --dest /tmp/insight-claw-pip-probe-pypi --index-url https://pypi.org/simple requests==2.32.5
.venv/bin/python -m pip download --no-cache-dir --no-deps --dest /tmp/insight-claw-pip-probe-tuna --index-url https://pypi.tuna.tsinghua.edu.cn/simple requests==2.32.5
```

If default PyPI is faster or the mirror fails, install normally:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

If the Tsinghua mirror is faster or default PyPI fails, use the mirror only for the current install command:

```bash
.venv/bin/python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

Do not write global `pip.conf`, `pip.ini`, or persistent pip index settings from this skill.

### Subsequent runs

When the repository and `.venv` already exist, run only the analysis command:

```bash
cd insight-claw
.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Do not automatically run `git pull` in an existing checkout. Reuse the local repository as-is unless the user explicitly asks for an update, or a failed run is traced to version or dependency drift. Before updating, inspect the local worktree state and ask for user approval.

Reinstall dependencies only after approved project updates, `requirements.txt` changes, or virtual environment failure.

## Runtime Requirements

Before running Insight Claw, confirm these requirements:

- Python 3.11+
- `git`
- `pip`
- `venv`
- Network access for dependency installation and configured data, search, LLM, or notification providers.
- Require at least one local LLM credential reference for real structured analysis. Prefer an existing `AIHUBMIX_KEY`; use `OPENAI_API_KEY` as fallback or primary key when appropriate. Secrets must stay local to the user's checkout or Hermes secret handling.

## Procedure

Follow the common local setup path first.

1. Locate an existing checkout by looking for `justice_plutus/`, `src/`, and `requirements.txt` in the working tree.
2. If no checkout exists, confirm the user wants to use the canonical repository `https://github.com/GeraltJc/insight-claw`, ask where the project should be stored, then download it with `git clone`.
3. Change into the repository directory.
4. Create an isolated Python environment with `python -m venv .venv`.
5. Before installing dependencies, compare default PyPI with `https://pypi.tuna.tsinghua.edu.cn/simple` using `pip download --no-cache-dir --no-deps`, then install with the faster successful index for this command only. Do not persist the selected index in pip configuration.
6. Before the first real analysis run, verify that a usable LLM credential is available through Hermes secret handling, the user's shell environment, or a user-approved local `.env` merge. If `.env` is missing and the user chooses local persistence, first create it from `.env.example` with `[ -f .env ] || cp .env.example .env`; then merge only missing keys or keys the user explicitly authorizes replacing. Prefer `AIHUBMIX_KEY` with OpenAI-compatible settings, or use `OPENAI_API_KEY` as fallback. Do not overwrite the whole `.env`. Do not collect, display, transmit, upload, or commit raw secret values.
7. Run the first validation without notifications:

```bash
.venv/bin/python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Equivalent command after activating the virtual environment:

```bash
python -m justice_plutus run --stocks 000001,600519 --workers 1 --no-notify
```

Use `--stocks` for a temporary self-selected stock override. It does not mutate the persistent `STOCK_LIST` configuration.

## Configuration

Keep configuration layered so the first run stays small:

| Layer | Variables | Purpose |
| --- | --- | --- |
| Required LLM path | `AIHUBMIX_KEY`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL` | Enables structured analysis and decision result generation. At least one usable key path is needed for real analysis. |
| Search enhancement | `BOCHA_API_KEYS`, `TAVILY_API_KEYS`, `SERPAPI_API_KEYS` | Adds search intelligence for risks, news, performance expectations, and industry context. Missing providers should degrade rather than block the whole pipeline. |
| Market data enhancement | `TUSHARE_TOKEN` | Improves行情数据 coverage. If unavailable, Insight Claw can continue through its data-source degradation chain where supported. |
| Chip distribution | `ENABLE_CHIP_DISTRIBUTION`, `WENCAI_COOKIE`, `HSCLOUD_AUTH_TOKEN` | Enables optional 筹码分布. Missing chip data should not stop the self-selected stock analysis pipeline. |
| TongHuaShun professional mode | `IFIND_REFRESH_TOKEN`, `ENABLE_THS_PRO_DATA`, `ENABLE_IFIND_ANALYSIS_ENHANCEMENT` | Enables optional 同花顺专业数据模式 for richer professional data. |
| Notification channels | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `FEISHU_WEBHOOK_URL` | Sends notification messages after reports are generated. Configure only after local no-notification validation passes. |

Use project terms consistently when explaining results:

- `行情数据`: historical daily bars and real-time quote facts.
- `搜索情报`: open search context used to enrich model input.
- `结构化分析`: model output in a parseable decision schema.
- `决策结果`: user-facing conclusion, risk, and action context.
- `分析报告`: local persisted report files.
- `批次汇总`: overview across all self-selected stocks in one run.
- `通知消息`: Telegram, Feishu, or another outbound message shape.
- `降级链`: the ordered fallback behavior for data sources, model routes, and notification outputs.

## Verification

Confirm that a no-notification validation run completes and produces reports:

- `reports/YYYY-MM-DD/stocks/<code>.md`
- `reports/YYYY-MM-DD/stocks/<code>.json`
- `reports/YYYY-MM-DD/summary.md`
- `reports/YYYY-MM-DD/summary.json`
- `reports/YYYY-MM-DD/run_meta.json`

## GitHub Actions

Use GitHub Actions only after the local flow is understood.

1. Configure GitHub Actions Secrets for secret values such as `AIHUBMIX_KEY`, `OPENAI_API_KEY`, `BOCHA_API_KEYS`, `TAVILY_API_KEYS`, `SERPAPI_API_KEYS`, `TUSHARE_TOKEN`, `TELEGRAM_BOT_TOKEN`, and optional provider tokens.
2. Configure GitHub Actions Variables for non-secret values such as `STOCK_LIST`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `MAX_WORKERS`, `REPORT_TYPE`, and `TELEGRAM_CHAT_ID` if the repository treats that chat id as non-secret.
3. Trigger `.github/workflows/justice_plutus_analysis.yml` with `workflow_dispatch`.
4. Use the `workflow_dispatch.stocks` input for a temporary self-selected stock override. This should not change the persistent `STOCK_LIST` variable.
5. Inspect the run status, generated artifacts, and notification channel separately. A notification failure does not necessarily mean analysis reports were not generated.

## Pitfalls

- Missing LLM credentials block real structured analysis. Use Hermes secret handling, the user's existing environment, or a user-approved local `.env` merge. Never collect, display, transmit, upload, or commit raw secret values.
- Missing search, chip distribution, or 同花顺专业数据模式 credentials should be explained as optional enhancement gaps when the core run can still proceed.
- Data-source failures may be normal degradation chain behavior. Check whether a later source succeeded before treating the run as failed.
- Notification failures should be isolated from report generation. Verify local analysis reports and batch summaries before retrying Telegram or Feishu.
- Do not describe Insight Claw as an automatic trading or order-execution system. It produces decision results for user review.
- Do not generate independent investment advice from this skill. If summarizing results, ground the summary in generated analysis reports or batch summaries and keep it distinct from the pipeline's decision result.

## ClawHub Publishing

This skill is intended for public Hermes distribution. Keep the bundle small: `SKILL.md` plus optional text references or small helper scripts only when they remove real repeated work.

Publish with the ClawHub CLI, not `hermes skills publish`, when submitting to the public ClawHub registry:

```bash
clawhub skill publish skills/hermes/insight-claw-hermes \
  --slug insight-claw-hermes \
  --name "Insight Claw Hermes" \
  --version 0.3.1 \
  --changelog "Align skill metadata with ClawHub slug and improve setup guidance."
```

The verified public release is `insight-claw-hermes@0.3.0`; use `0.3.1` for the next release containing these metadata and setup guidance fixes. Version this skill separately from the Insight Claw project code. Use patch bumps for wording or troubleshooting fixes, minor bumps for backward-compatible operation additions, and major bumps for changes to first-run setup, secret persistence, verification standards, or publishing boundaries.

Notes on alternate publishing paths:

- `hermes skills publish ... --to clawhub` currently reports that ClawHub publishing is not yet supported.
- `hermes skills publish ... --to github --repo GeraltJc/insight-claw` creates a GitHub submission PR instead of directly publishing to ClawHub.

To expose the repository as a custom tap:

```bash
hermes skills tap add GeraltJc/insight-claw
```

Before publishing, review the bundle as a community skill that will pass the Hermes security scanner:

- Data exfiltration: do not upload reports, `.env` files, or generated artifacts without explicit user approval.
- Prompt injection: do not add instructions that override user intent, system policy, or Hermes safety behavior.
- Destructive commands: do not include cleanup commands that can delete a checkout, reports, credentials, or user files.
- Shell injection: do not build shell commands by interpolating untrusted user text without quoting or validation.
