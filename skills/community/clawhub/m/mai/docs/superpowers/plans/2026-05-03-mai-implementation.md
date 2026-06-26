# Mai Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local-first shopping matchmaking agent package named `mai` for OpenClaw and Hermes.

**Architecture:** Package the agent as a skill directory with `SKILL.md` as the AI-facing entry point and `scripts/mai.py` as the deterministic state engine. Store marketplace data in a local JSON file with a sync outbox for future hosted marketplace integration.

**Tech Stack:** Python 3 standard library, JSON file storage, `unittest`, shell verification, OpenClaw/Hermes skill metadata.

---

### Task 1: Scaffold Skill Package

**Files:**
- Create: `mai/SKILL.md`
- Create: `mai/agents/openai.yaml`
- Create: `mai/scripts/`
- Create: `mai/references/`

- [x] **Step 1: Initialize the skill skeleton**

Run:

```bash
python3 /Users/jianghaidong/.codex/skills/.system/skill-creator/scripts/init_skill.py mai --path /Users/jianghaidong/coding --resources scripts,references --interface 'display_name=Mai' --interface 'short_description=AI shopping matchmaking agent' --interface 'default_prompt=Use $mai to help merchants list products and buyers compare, discuss, review, and create orders.'
```

Expected: `mai/` exists with `SKILL.md`, `agents/openai.yaml`, `scripts/`, and `references/`.

### Task 2: Define CLI Behavior With Tests

**Files:**
- Create: `mai/tests/test_cli.py`

- [x] **Step 1: Write failing workflow tests**

Cover:

- merchant creation
- product publishing
- review creation
- product search
- SKU comparison
- buyer/merchant message recording
- order creation, quote, confirmation, external payment, fulfillment, completion
- insufficient stock rejection
- invalid order transition rejection

- [x] **Step 2: Run tests and confirm RED**

Run:

```bash
python3 -m unittest discover -s mai/tests
```

Expected: fail because `scripts/mai.py` has no `main()`.

### Task 3: Implement Deterministic State Engine

**Files:**
- Create: `mai/scripts/mai.py`

- [x] **Step 1: Implement JSON store and argparse command tree**

Implement global `--data`, local default path, and commands:

- `merchant create/list`
- `product add/stock/list`
- `search products/merchants`
- `compare`
- `review add/list`
- `message add/list`
- `order create/quote/update/show/list`

- [x] **Step 2: Implement order state machine**

Allowed happy path:

```text
draft -> quoted -> confirmed -> payment_pending -> paid_external -> fulfilled -> completed
```

Dispute path:

```text
disputed -> resolved/refunded/cancelled
```

Reserve stock on `confirmed`; release stock on `cancelled` or `refunded`.

- [x] **Step 3: Run tests and confirm GREEN**

Run:

```bash
python3 -m unittest discover -s mai/tests
```

Expected: all tests pass.

### Task 4: Package Agent Instructions and Metadata

**Files:**
- Modify: `mai/SKILL.md`
- Create: `mai/README.md`
- Create: `mai/package.json`
- Create: `mai/clawhub.json`
- Modify: `mai/agents/openai.yaml`

- [x] **Step 1: Replace placeholder skill instructions**

Include operating principles, merchant workflow, buyer workflow, transaction model, output expectations, and verification commands.

- [x] **Step 2: Add install and publish documentation**

Document OpenClaw symlink install, Hermes local install, and Hermes publish command.

- [x] **Step 3: Add ecosystem metadata**

Ensure `package.json`, `clawhub.json`, and `agents/openai.yaml` use `mai` consistently.

### Task 5: Add References and Verification

**Files:**
- Create: `mai/references/transaction-model.md`
- Create: `mai/references/data-schema.md`
- Create: `mai/scripts/verify.sh`

- [x] **Step 1: Document transaction safety**

Describe statuses, allowed flows, stock reservation, external payment tracking, and dispute handling.

- [x] **Step 2: Document schema and sync outbox**

Describe merchants, products, orders, messages, reviews, inventory events, and `sync.pending_events`.

- [x] **Step 3: Implement verification script**

Run CLI help, unit tests, smoke workflow, JSON assertions, metadata consistency assertions, and placeholder scan.

### Task 6: Final Verification

**Files:**
- Inspect all package files.

- [x] **Step 1: Run unit tests**

Run:

```bash
python3 -m unittest discover -s mai/tests
```

Expected: all tests pass.

- [x] **Step 2: Run package verifier**

Run:

```bash
bash mai/scripts/verify.sh
```

Expected: `verification ok`.

- [x] **Step 3: Run skill validator**

Run:

```bash
python3 /Users/jianghaidong/.codex/skills/.system/skill-creator/scripts/quick_validate.py mai
```

Expected: validation passes.

- [x] **Step 4: Audit objective coverage**

Check every explicit objective requirement against concrete files and command output before marking the goal complete.

### Task 7: Registry Marketplace Extension

**Files:**
- Create: `mai/tests/test_registry.py`
- Create: `mai/scripts/mai_registry.py`
- Modify: `mai/scripts/mai.py`
- Create: `mai/references/registry-api.md`
- Modify: `mai/README.md`
- Modify: `mai/SKILL.md`
- Modify: `mai/package.json`

- [x] **Step 1: Write failing registry integration test**

Cover merchant push, buyer registry search, buyer registry message, buyer registry order, merchant pull, and registry persistence.

- [x] **Step 2: Implement registry HTTP service**

Add `GET /health`, `POST /sync/push`, `GET /search/products`, `GET /search/merchants`, `POST /messages`, `POST /orders`, and `GET /merchants/{merchant_id}/inbox`.

- [x] **Step 3: Implement CLI registry commands**

Add `registry push`, `registry search-products`, `registry search-merchants`, `registry message`, `registry order`, and `registry pull`.

- [x] **Step 4: Update docs and verifier**

Document registry usage, add `mai-registry` bin metadata, and include registry help/test coverage in verification.

### Task 8: Public Marketplace Controls

**Files:**
- Create: `mai/tests/test_public_marketplace.py`
- Modify: `mai/scripts/mai_registry.py`
- Modify: `mai/scripts/mai.py`
- Modify: `mai/references/registry-api.md`
- Create: `mai/references/public-deployment.md`
- Modify: `mai/README.md`
- Modify: `mai/SKILL.md`

- [x] **Step 1: Write failing public marketplace tests**

Cover unauthenticated rejection, merchant/buyer/admin authorization, API key hashing, rate limiting, risk moderation, moderation approval, demo payment hold, unauthorized release rejection, and admin release.

- [x] **Step 2: Add registry authentication and authorization**

Implement `issue-key`, salted API key hashes, Bearer authentication, merchant scope, buyer scope, and admin-only operations.

- [x] **Step 3: Add rate limiting**

Track per-minute request counts by API key id or client IP. Return HTTP 429 after the configured limit.

- [x] **Step 4: Add risk scoring and moderation**

Score product risk on push, hide risky products, expose admin moderation queue, and implement approve/reject decisions.

- [x] **Step 5: Add PSP-backed payment custody records**

Add demo payment hold/release/refund endpoints and CLI commands. Require buyer keys for holds and admin keys for release/refund.

- [x] **Step 6: Update public deployment docs**

Document the security controls, live PSP boundary, and production checklist.

- [x] **Step 7: Add container deployment assets**

Add `Dockerfile`, `docker-compose.yml`, and `registry.example.env` for registry service deployment behind HTTPS.

### Task 9: OpenClaw and Hermes Installer

**Files:**
- Create: `mai/tests/test_install.py`
- Create: `mai/scripts/install.sh`
- Modify: `mai/scripts/verify.sh`
- Modify: `mai/README.md`
- Modify: `mai/SKILL.md`
- Modify: `mai/package.json`

- [x] **Step 1: Write failing installer tests**

Cover OpenClaw symlink install, Hermes symlink install, dry-run behavior, and refusing to overwrite existing targets without `--force`.

- [x] **Step 2: Implement installer**

Add `bash scripts/install.sh --both|--openclaw|--hermes [--dry-run] [--force]` with `OPENCLAW_HOME` and `HERMES_HOME` overrides.

- [x] **Step 3: Update docs and verifier**

Document one-command install for users and include installer dry-run in `scripts/verify.sh`.
