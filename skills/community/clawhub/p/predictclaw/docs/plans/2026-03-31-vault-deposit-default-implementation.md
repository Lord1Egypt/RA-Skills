# Vault Deposit Default Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make `predict-account + vault` default funding guidance point at the Vault deposit flow instead of the Predict Account address.

**Architecture:** Keep the internal route identifier `vault-to-predict-account`, but rewrite user-facing guidance fields, CLI text, and docs so funding ingress = Vault and trading identity = Predict Account.

**Tech Stack:** Python CLI/output shaping, pytest, Markdown docs.

---

### Task 1: Lock user-facing funding semantics in tests

**Files:**
- Modify: `tests/test_funding.py`
- Modify: `tests/test_cli_router.py`
- Modify: `tests/test_docs_examples.py`

**Step 1: Write failing tests**
- Assert overlay `fundingAddress` and `manualTopUpAddress` are the Vault.
- Assert human-readable wallet deposit output labels Vault as the default funding entry.
- Assert docs describe Vault deposit flow as the default ingress.

**Step 2: Run focused tests to verify RED**
- `uv run pytest tests/test_funding.py tests/test_cli_router.py tests/test_docs_examples.py -q`

### Task 2: Change JSON/output semantics

**Files:**
- Modify: `lib/wallet_manager.py`
- Modify: `lib/funding_service.py`
- Modify: `scripts/wallet.py`

**Step 1: Update guidance fields**
- Point overlay `fundingAddress` to the Vault.
- Point `manualTopUpAddress` to the Vault.
- Rewrite guidance string to explain vault-first funding.

**Step 2: Update CLI labels**
- Replace the old manual top-up phrasing with Vault deposit flow wording.

**Step 3: Run focused tests to verify GREEN**
- `uv run pytest tests/test_funding.py tests/test_cli_router.py -q`

### Task 3: Rewrite docs/help text

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `SKILL.md`
- Modify: `scripts/predictclaw.py`

**Step 1: Rewrite funding-address guidance**
- Make Vault deposit flow the default answer for `predict-account + vault`.
- Keep Predict Account as trading identity.

**Step 2: Run docs tests to verify GREEN**
- `uv run pytest tests/test_docs_examples.py -q`

### Task 4: Final verification and release

**Step 1: Run full tests**
- `uv run pytest -q`

**Step 2: If publishing is requested, bump version and release**
