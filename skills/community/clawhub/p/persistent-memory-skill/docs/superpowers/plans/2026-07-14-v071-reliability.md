# v0.7.1 Reliability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Persistent Memory's published instructions, lifecycle operations, onboarding, and release metadata truthful, safe, and verifiable for an existing local memory system.

**Architecture:** Keep the product as a portable instruction-only skill. Add a Node built-in-test contract suite that reads the four Markdown documents and protects product promises from regressing. The skill gains an explicit `memory upgrade` flow and constrained lifecycle operations; README files explain the same runtime contract in English and Chinese.

**Tech Stack:** Markdown, SVG, Node.js 24 built-in `node:test`, Git.

## Global Constraints

- Modify only the isolated worktree at `C:\Users\Yui\.agents\skills\persistent-memory\.worktrees\v071-reliability`.
- Do not modify `C:\Users\Yui\.persistent-memory` user data during implementation or tests.
- Do not claim that section-summary loading is a current v0.7.1 feature.
- Cross-agent sharing requires one shared local filesystem, compatible agents, discovered skill instructions, and appropriate file permissions.
- Lifecycle commands must accept only normalized relative paths inside `~/.persistent-memory/` and must protect `_core/`, `_index.md`, `_archive/_index.md`, and hidden metadata.
- Every mutation of memory content or lifecycle structure requires an explicit user confirmation after a preview.

---

## File Structure

- Create: `tests/skill-contract.test.mjs` — executable assertions covering the documentation and lifecycle contract.
- Create: `CHANGELOG.md` — v0.7.1 release notes and an explicit correction for the no-longer-current Summary-first behavior.
- Modify: `SKILL.md` — English agent behavior contract, upgrade flow, safety limits, and corrected archive semantics.
- Modify: `SKILL_zh.md` — Chinese mirror of the same behavior contract.
- Modify: `README.md` — English onboarding, compatibility conditions, upgrade instructions, data-boundary guidance, and release link.
- Modify: `README_zh.md` — Chinese mirror of the same user-facing contract.
- Modify: `architecture.svg` — diagram showing lifecycle storage and the conditions under which agents share memory.

### Task 1: Add an executable contract suite

**Files:**
- Create: `tests/skill-contract.test.mjs`

**Interfaces:**
- Consumes: `SKILL.md`, `SKILL_zh.md`, `README.md`, `README_zh.md` as UTF-8 text.
- Produces: `node --test tests/skill-contract.test.mjs` with one named assertion per published behavior.

- [ ] **Step 1: Write the failing test**

```js
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const read = (file) => readFile(new URL(`../${file}`, import.meta.url), 'utf8');

test('documents an explicit upgrade path for existing memory', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);
  assert.match(en, /### Upgrade Existing Memory/);
  assert.match(zh, /### 升级已有记忆/);
  assert.match(en, /memory upgrade/);
  assert.match(zh, /升级记忆/);
});

test('limits lifecycle paths and protects core memory', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);
  for (const text of [en, zh]) {
    assert.match(text, /relative path/i);
    assert.match(text, /_core/);
    assert.match(text, /_archive\/_index\.md/);
  }
});

test('states the cross-agent sharing conditions without claiming full-context loading', async () => {
  const [en, zh] = await Promise.all([read('README.md'), read('README_zh.md')]);
  assert.match(en, /same local filesystem/i);
  assert.match(en, /compatible agent/i);
  assert.match(en, /baseline context/i);
  assert.doesNotMatch(en, /Loads your full context/);
  assert.match(zh, /同一.*本地文件系统/);
  assert.match(zh, /基础上下文/);
});

test('keeps raw repositories and media outside managed memory', async () => {
  const [en, zh] = await Promise.all([read('README.md'), read('README_zh.md')]);
  assert.match(en, /raw repositories, downloads, media files, and datasets/i);
  assert.match(zh, /原始仓库、下载文件、媒体文件和数据集/);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/skill-contract.test.mjs`

Expected: FAIL because `tests/skill-contract.test.mjs` does not exist.

- [ ] **Step 3: Create the test file unchanged**

Create `tests/skill-contract.test.mjs` with the exact code from Step 1.

- [ ] **Step 4: Run test to verify it fails for missing v0.7.1 behavior**

Run: `node --test tests/skill-contract.test.mjs`

Expected: FAIL on the upgrade, lifecycle-path, compatibility, and data-boundary assertions.

### Task 2: Make lifecycle operations safe and upgradeable

**Files:**
- Modify: `SKILL.md`
- Modify: `SKILL_zh.md`
- Test: `tests/skill-contract.test.mjs`

**Interfaces:**
- Consumes: a user command plus a path relative to `~/.persistent-memory/`.
- Produces: an explicit preview and confirmation before creating lifecycle folders or moving any file.

- [ ] **Step 1: Add failing assertions for the v0.7.1 lifecycle rules**

Append these tests to `tests/skill-contract.test.mjs`:

```js
test('requires explicit confirmation before lifecycle migration or mutation', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);
  assert.match(en, /explicit user confirmation/i);
  assert.match(zh, /用户明确确认/);
});

test('does not present Summary-first loading as a current feature', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);
  assert.doesNotMatch(en, /100 lines or more.*Summary/s);
  assert.doesNotMatch(zh, /100 行及以上.*Summary/s);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/skill-contract.test.mjs`

Expected: FAIL because the current skill has neither the upgrade confirmation contract nor the v0.7.1 lifecycle path rules.

- [ ] **Step 3: Update both skill files**

In both languages:

1. Replace the malformed directory tree with three explicit states: `_core/`, active on-demand files indexed by `_index.md`, and `_archive/` with `_trash/`.
2. State that `load memory` loads **baseline context** (`_core/` and `_index.md`) only after the skill is active; on-demand files are loaded separately.
3. Add `Upgrade Existing Memory` / `升级已有记忆`, triggered by `memory upgrade` / `升级记忆`. It previews any missing `_archive/`, `_archive/_trash/`, and `_archive/_index.md`, waits for explicit confirmation, creates only missing structure, and never moves or rewrites existing active files.
4. Before `archive`, `delete`, `recover`, or `memory health`, require the lifecycle structure. If it is missing, direct the agent to the upgrade flow and do not mutate files.
5. Require normalized relative paths, reject absolute paths and `..`, verify resolved paths remain under the memory root, and reject `_core/`, root control files, hidden metadata, and archive-index operations.
6. Permit archive only for active on-demand files; require an active file to be archived before it can be deleted. Permit recovery only from `_archive/` or `_archive/_trash/`.
7. Replace the contradictory archive question with this three-way rule: active for current or near-term work; archive for completed low-frequency material with plausible future reference value; delete only for clearly obsolete or duplicate material after confirmation.
8. Correct the duplicate numbered initialization step and keep Chinese and English behavior equivalent.

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test tests/skill-contract.test.mjs`

Expected: PASS for lifecycle and Summary-first assertions; README assertions may remain failing until Task 3.

### Task 3: Correct onboarding, boundaries, and versioned public artifacts

**Files:**
- Modify: `README.md`
- Modify: `README_zh.md`
- Modify: `architecture.svg`
- Create: `CHANGELOG.md`
- Test: `tests/skill-contract.test.mjs`

**Interfaces:**
- Consumes: the v0.7.1 skill behavior from Task 2.
- Produces: user-facing docs that describe the same activation, compatibility, data-boundary, upgrade, and lifecycle contract.

- [ ] **Step 1: Update README files**

In both languages:

1. Change the hero promise from “replaces all built-in memory” to a complementary shared local memory layer.
2. Change Quick Start to require an explicit first command such as `remember this` / `记住这个`, rather than promising a proactive save prompt.
3. Replace “Loads your full context” with “Loads baseline context: core files and the index.”
4. Add a `Compatibility contract` section: same local filesystem, compatible agent that can discover the skill or an equivalent fallback, same user-accessible memory path, and read/write permissions; platform memories may coexist.
5. Add an `Upgrade existing memory` section that sends users to `memory upgrade` / `升级记忆` before lifecycle commands if their system predates v0.7.
6. Add `What belongs in memory`: stable context, decisions, concise project state, and pointers; raw repositories, downloads, media files, and datasets remain in their project workspaces.
7. Render the directory tree in a fenced code block and include `_archive/_trash/`.

- [ ] **Step 2: Update architecture.svg and CHANGELOG.md**

1. Extend the diagram’s central storage label to include the active index, archive, and trash lifecycle, and add a caption that local sharing requires compatible agents on the same filesystem.
2. Create `CHANGELOG.md` with a `v0.7.1` section dated `2026-07-14`. List: explicit upgrade path; path/core safety; corrected activation and compatibility wording; memory-vs-source-material boundary; corrected documentation; and the fact that Summary-first loading is not included in this release.

- [ ] **Step 3: Run test to verify it passes**

Run: `node --test tests/skill-contract.test.mjs`

Expected: all tests PASS.

- [ ] **Step 4: Run static release checks**

Run:

```powershell
node --test tests/skill-contract.test.mjs
git diff --check
git status --short
```

Expected: tests pass, `git diff --check` returns no output, and only the seven planned files are modified or created.

### Task 4: Verify agent-facing behavior and commit

**Files:**
- Test: `SKILL.md`, `SKILL_zh.md`, `tests/skill-contract.test.mjs`

**Interfaces:**
- Consumes: v0.7.1 text and a temporary memory fixture outside `~/.persistent-memory/`.
- Produces: a recorded acceptance matrix for baseline loading, migration, archive safety, delete safety, recovery, and cross-agent setup readiness.

- [ ] **Step 1: Run deterministic acceptance checks against a temporary fixture**

Create a temporary fixture under the worktree’s ignored `.tmp/` directory with an active project file, `_core/profile.md`, `_index.md`, and no lifecycle folders. Verify the documented upgrade preview would create only missing lifecycle folders; verify archive/delete path guards reject `_core/profile.md`, `../outside.md`, and an absolute path; verify an on-demand file is eligible for archive; verify recovery is only eligible from archive/trash. Remove the fixture after recording the result.

- [ ] **Step 2: Run agent scenario review**

Use three scenarios against `SKILL.md` and `SKILL_zh.md`:

1. An existing user asks to delete `projects/old.md` without `_trash/` present; the expected answer is an upgrade preview and confirmation, not a move.
2. A user asks to archive `_core/profile.md`; the expected answer refuses because core files are protected.
3. A new user asks whether Claude and Codex “automatically share everything”; the expected answer names the filesystem, discovery, path, and permission conditions and says baseline context is not full content.

Record pass/fail in the final implementation report.

- [ ] **Step 3: Commit the implementation**

Run:

```powershell
git add CHANGELOG.md README.md README_zh.md SKILL.md SKILL_zh.md architecture.svg tests/skill-contract.test.mjs docs/superpowers/plans/2026-07-14-v071-reliability.md
git commit -m "feat: harden persistent memory lifecycle"
```

Expected: one implementation commit on `codex/v071-reliability`.

## Self-Review

- Scope coverage: Task 2 implements migration, path safety, core protection, archive semantics, and truthful Summary-first status. Task 3 reconciles public artifacts and data boundaries. Task 4 verifies the documented behavior before release.
- Placeholder scan: this plan contains no TBD/TODO placeholders and each implementation task names exact files and commands.
- Consistency: all tests use `node --test tests/skill-contract.test.mjs`; all lifecycle instructions use `memory upgrade` / `升级记忆` and the same protected paths.
