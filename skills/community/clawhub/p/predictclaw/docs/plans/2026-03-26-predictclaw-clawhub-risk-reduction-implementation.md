# PredictClaw ClawHub Risk Reduction Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reduce the likelihood that PredictClaw is flagged as suspicious on ClawHub by removing default auto-install and auto-write behavior, making the setup path safe by default, and documenting the external MCP runtime explicitly.

**Architecture:** Keep mandated-vault and overlay runtime support intact, but change setup and documentation so the default path only detects the external `erc-mandated-mcp` launcher and prints manual instructions. Remove runtime code paths that perform global npm install or write `.env` automatically from the published skill package.

**Tech Stack:** Python 3.11+, pytest, PredictClaw CLI, ClawHub-published skill docs.

---

### Task 1: Lock the new safe-default setup contract in tests

**Files:**
- Modify: `tests/test_mandated_mcp_setup.py`
- Modify: `tests/test_cli_router.py`
- Modify: `tests/test_docs_examples.py`

**Step 1: Write failing setup tests**

- Replace tests that expect auto-install and auto `.env` backfill with tests that expect detection-only behavior.
- Assert setup help no longer advertises `--install` / `--write-env`.
- Assert docs no longer present the one-click install/write-env path as the normal workflow.

**Step 2: Run tests to verify RED**

Run: `uv run pytest tests/test_mandated_mcp_setup.py tests/test_cli_router.py tests/test_docs_examples.py -q`

### Task 2: Remove auto-install and auto-write behavior from setup

**Files:**
- Modify: `lib/mandated_mcp_setup.py`
- Modify: `scripts/setup.py`
- Delete: `lib/env_backfill.py` if it is unused
- Test: `tests/test_mandated_mcp_setup.py`
- Test: `tests/test_cli_router.py`

**Step 1: Make configure_mandated_mcp detection-only**

- Remove runtime `npm install -g` behavior from the published code path.
- Remove automatic `.env` writes from setup.
- Return a manual instruction message when the launcher is missing.

**Step 2: Simplify setup CLI**

- Remove `--install` and `--write-env` flags from the public setup command.
- Keep the command as a safe detector that prints what runtime is required and what env var the user must set manually.

**Step 3: Run focused tests to verify GREEN**

Run: `uv run pytest tests/test_mandated_mcp_setup.py tests/test_cli_router.py -q`

### Task 3: Make the external MCP runtime explicitly declared in docs

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `SKILL.md`
- Test: `tests/test_docs_examples.py`

**Step 1: Update main-path docs**

- Rewrite mandated MCP setup docs so the default path says:
  - PredictClaw depends on an external `erc-mandated-mcp` runtime
  - users must install/configure it separately
  - PredictClaw does not globally install packages or auto-edit `.env` as the default path

**Step 2: Keep advanced behavior out of the normal path**

- If any advanced recovery behavior remains documented, clearly mark it as advanced/manual and not the recommended path.
- Remove one-click auto-install framing from README/SKILL examples and notes.

**Step 3: Run focused docs tests to verify GREEN**

Run: `uv run pytest tests/test_docs_examples.py tests/test_skill_manifest.py -q`

### Task 4: Final verification and publication readiness

**Files:**
- Modify only if verification reveals gaps

**Step 1: Run targeted regression suite**

Run: `uv run pytest tests/test_mandated_mcp_setup.py tests/test_cli_router.py tests/test_docs_examples.py tests/test_skill_manifest.py -q`

**Step 2: Run full suite**

Run: `uv run pytest -q`

**Step 3: Run CLI help checks**

Run:
- `uv run python scripts/predictclaw.py --help`
- `uv run python scripts/setup.py --help`

**Step 4: Publish follow-up**

- Bump version
- Sync to GitHub
- Publish to ClawHub
- Re-check the ClawHub page state
