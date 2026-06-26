# Vault Mode Semantics Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite PredictClaw docs/help/templates so only four user-facing modes remain visible while `mandated-vault` is repositioned as an internal bootstrap/compatibility detail.

**Architecture:** Keep runtime behavior unchanged. Add a canonical `predict-account + vault` template, demote `template.mandated-vault.env` to internal/compatibility status, and update docs/tests/help text to enforce the user-facing semantic split.

**Tech Stack:** Markdown docs, env templates, Python CLI help text, pytest docs/template tests.

---

### Task 1: Lock the new semantic contract in tests

**Files:**
- Modify: `tests/test_docs_examples.py`
- Modify: `tests/test_scaffold.py`

**Step 1: Write failing docs tests**

- Assert docs describe four user-facing modes.
- Assert docs present `predict-account + vault` as the canonical vault-enabled route.
- Assert `template.predict-account-vault.env` exists and appears in first-install guidance.
- Assert `template.mandated-vault.env` is described as internal/compatibility bootstrap, not a user-facing mode.

**Step 2: Run focused tests to verify RED**

Run: `uv run pytest tests/test_docs_examples.py tests/test_scaffold.py -q`

### Task 2: Add the canonical predict-account + vault template

**Files:**
- Create: `template.predict-account-vault.env`
- Create: `.env.predict-account-vault.example`
- Modify: `template.env`

**Step 1: Add the new template**

- Keep `PREDICT_WALLET_MODE=predict-account`
- Include the vault-binding envs needed after a vault exists
- Explain that if the vault does not exist yet, users should run `wallet bootstrap-vault` first

**Step 2: Reframe the old mandated-vault template**

- Keep the file for compatibility
- Rewrite comments so it is explicitly internal/bootstrap-oriented

**Step 3: Run template tests to verify GREEN**

Run: `uv run pytest tests/test_scaffold.py -q`

### Task 3: Rewrite README and README.zh-CN

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`

**Step 1: Rewrite the mode list**

- Remove user-facing wording that presents `mandated-vault` as a mode
- Present only the four user-facing modes

**Step 2: Rewrite vault onboarding**

- Explain `predict-account + vault` as the advanced route
- Explain the “create vault first or bind existing vault” decision tree
- Explicitly call `mandated-vault` an internal bootstrap subflow

**Step 3: Run docs tests to verify GREEN**

Run: `uv run pytest tests/test_docs_examples.py -q`

### Task 4: Rewrite SKILL.md and CLI help

**Files:**
- Modify: `SKILL.md`
- Modify: `scripts/predictclaw.py`

**Step 1: Align skill documentation**

- Reframe `wallet bootstrap-vault` as part of `predict-account + vault` onboarding
- Clarify internal/bootstrap-only references to `mandated-vault`

**Step 2: Align top-level help text**

- Remove wording that implies `mandated-vault` is a user-facing mode
- Add wording that `mandated-vault` exists as an internal bootstrap subflow

**Step 3: Run help/docs verification**

Run:
- `uv run python scripts/predictclaw.py --help`
- `uv run pytest tests/test_docs_examples.py -q`

### Task 5: Final verification

**Files:**
- No new files unless verification reveals a small doc/test gap

**Step 1: Run focused docs/template suite**

Run: `uv run pytest tests/test_docs_examples.py tests/test_scaffold.py -q`

**Step 2: Run full test suite**

Run: `uv run pytest -q`

**Step 3: If user asks for publishing, then commit/push/publish**

Keep commits doc-focused and atomic.
