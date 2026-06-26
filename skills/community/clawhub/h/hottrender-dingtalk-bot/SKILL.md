---
name: hottrender-dingtalk-bot
description: Use when users need a lightweight HotTrender crawler for four-region daily hotspot trends or custom keyword/vertical hotspot discovery. Prefer the bundled basic crawler runtime and existing provider scripts before writing code. This skill intentionally excludes DingTalk push, OSS publishing, ActionCard pages, lp-ads workspace, worker queues, databases, and LLM summaries.
---

# HotTrender Basic Crawler

## Core Rule

For four-region daily hotspot trends or vertical/custom-keyword hotspot discovery, use the bundled crawler runtime first. Do not reimplement platform crawling until the existing providers and scripts are checked.

Before changing code, answer these questions:

1. Is there already a script, API, provider, doc, or test covering this need?
2. Can the user goal be satisfied by running or configuring that capability?
3. If not, what exact gap remains, and where is the smallest extension point?

Only edit code after that evaluation.

## Repository Layout

This skill bundles a sanitized basic crawler runtime under `assets/hottrender-runtime/`. It does not bundle DingTalk, OSS, ActionCard, lp-ads, worker queues, databases, logs, LLM, or any secrets.

First resolve the runtime path from environment variables, the current workspace, or the bundled runtime:

```text
HOTTRENDER_APP_DIR   # directory containing scripts/fetch_daily_trends.py
```

If `HOTTRENDER_APP_DIR` is missing, install the bundled runtime:

```bash
python assets/install_hottrender_runtime.py --target ./HotTrenderRuntime
export HOTTRENDER_APP_DIR="$PWD/HotTrenderRuntime"
```

If variables are missing but a local checkout may exist, discover it safely:

```bash
find "$PWD" "$HOME" -maxdepth 5 -path '*/scripts/fetch_daily_trends.py' 2>/dev/null
```

## Fast Path

Use these references only when needed:

- Setup requirements and portability constraints: [setup.md](references/setup.md)
- Daily trend and custom keyword commands: [commands.md](references/commands.md)
- Existing provider capabilities and extension points: [capabilities.md](references/capabilities.md)
- How to decide whether to configure, run, or modify code: [extension-policy.md](references/extension-policy.md)

## Operating Workflow

1. For "四地区热点", "每日热点", "daily trends", or "jp/us/tw/kr", start from `scripts/fetch_daily_trends.py`.
2. For "垂类热点", "关键词热点", "自定义关键词", or "custom keyword", start from `scripts/fetch_keyword_hotspots.py`.
3. For "抓取是否有效", "平台数据不对", or "为什么没结果", inspect `configs/providers.yaml`, run offline mode first, then real mode.
4. For code changes, keep the runtime basic. Do not add DingTalk, OSS, lp-ads, database, worker, or LLM features back into this skill.

## Guardrails

- Never print API keys, cookies, tokens, msToken, proxy credentials, or other secrets.
- Do not fabricate live platform data. Offline/sample mode must be called out as offline/sample.
- Do not introduce push, publishing, database, queue, or workspace features into this basic crawler.
- If the user has no HotTrender checkout, use the bundled runtime installer before proposing code rewrites.
- Keep changes scoped: provider logic in `src/providers`, orchestration in `src/crawler.py`, CLI entrypoints in `scripts/`.

## Verification

Prefer focused verification:

```bash
cd "$HOTTRENDER_APP_DIR"
python -m pytest tests/test_basic_crawler.py -q
python scripts/fetch_daily_trends.py --config configs/providers.yaml --output out/daily_trends.md
```
