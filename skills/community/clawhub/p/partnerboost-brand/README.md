**English** · [简体中文](README.zh-CN.md)

# PartnerBoost Merchant API Skill

This repository provides an **AI Agent Skill** for the PartnerBoost **merchant** side. Agents use natural language to drive `curl` calls against the same WebUI-backed APIs, for orders, performance analytics, billing, account data, and more.

Full Skill instructions and API reference: [`SKILL.md`](./SKILL.md).

## When to use it

- Automate merchant-side queries and summaries in Agent runtimes that support this Skill (e.g. OpenClaw, QClaw, Wukong when configured)
- Single source of truth for auth (`X-Api-Key`) and base URL

## Skill metadata

| Field | Value |
|-------|--------|
| Name | `partnerboost-api` |
| Version | 1.1.1 |
| Tags | partnerboost, api, merchant |

## Prerequisites

1. **API key** — request a merchant API key from your CSM.
2. **Environment** — the Agent must have access to `PARTNERBOOST_API_KEY` (see below).

## Installation

### Skills CLI (`npx skills add`)

Use the [Skills CLI](https://skills.sh/docs/cli) (no global install needed):

```bash
npx skills add <owner>/<repo>
```

Anyone can install from **this repository’s address** on your Git host (GitHub `owner/repo`, a full repo URL, or another format the [Skills CLI](https://skills.sh/docs/cli) accepts). Use the `owner/repo` shown on the repo home page, for example:

```bash
npx skills add OWNER/partnerboost-brand
```

Run `npx skills add --help` for flags such as `-g` / `--global` and `-a` / `--agent` (target Cursor, Claude Code, OpenCode, etc.).

You still need **`PARTNERBOOST_API_KEY`** wherever your agent loads secrets (see **OpenClaw / QClaw** below, or your editor’s env / secrets UI).

### API key for OpenClaw-compatible clients

**OpenClaw** and **QClaw** own config location and how env vars are passed. This Skill does not prescribe a file path or JSON schema—only that **`PARTNERBOOST_API_KEY`** is available when runs execute. Follow each client’s docs.

### OpenClaw

Register this repo’s [`SKILL.md`](./SKILL.md) as **`partnerboost-api`** using the flow described in [OpenClaw Skills config](https://docs.openclaw.ai/tools/skills-config).

### QClaw

**QClaw** is Tencent’s packaged OpenClaw client (WeChat remote control, ClawHub, optional reuse of an existing OpenClaw setup).

1. Install from [QClaw](https://qclaw.qq.com) and finish onboarding (channels, model, etc.).
2. **Skills:** open **Skills** in the sidebar — install from ClawHub, or add this project as a **custom / GitHub-style** skill if your build supports it.
3. Add this Skill through the client’s UI or the custom-skill flow described in QClaw / OpenClaw documentation.
4. Provide **`PARTNERBOOST_API_KEY`** exactly as your client documents (not duplicated here).

Unofficial walkthrough (Chinese): [qclaw.run](https://www.qclaw.run/zh/) — e.g. [install guide](https://www.qclaw.run/zh/qclaw-anzhuang-jiaocheng/) (includes a **Skills** step).

### Wukong (悟空)

**Wukong** is Alibaba’s enterprise Agent platform (DingTalk AI / standalone app). It ships with an AI capability marketplace and is described as compatible with open Skill-style content.

1. In **Wukong** or **DingTalk** (per your org’s rollout), open the skill / capability entry your admin uses (marketplace, custom skill upload, or developer workflow).
2. Import or register this repository’s [`SKILL.md`](./SKILL.md) under the name **`partnerboost-api`** (or the identifier your platform requires).
3. Configure **`PARTNERBOOST_API_KEY`** in the platform’s environment, secrets, or skill settings (wording varies by version).

Availability (invite / beta) and exact menus change with product updates — follow **DingTalk AI** and **Wukong** official documentation.

## API overview

- **Base URL:** `https://app.partnerboost.com`
- **Auth:** every request needs `X-Api-Key: $PARTNERBOOST_API_KEY`
- **Conventions:** GET/POST URL shape, JSON shape (`code` / `message` / `data`), and pagination fields are documented in [`SKILL.md`](./SKILL.md)

Documented areas:

| Area | What it covers |
|------|----------------|
| Transaction | Order list, stats, recent orders |
| Performance | Charts, paged list, totals, partner search |
| Account / Billing | Billing list, account info, current plan, prepayment records |

## Repository layout

```
.
├── README.md        # This file (English)
├── README.zh-CN.md  # 简体中文
└── SKILL.md         # Skill definition and full API reference
```

## Compliance

Usage limits, rate limits, and compliance follow PartnerBoost’s official terms and your contract. Do not expose API keys in logs or chat transcripts.
