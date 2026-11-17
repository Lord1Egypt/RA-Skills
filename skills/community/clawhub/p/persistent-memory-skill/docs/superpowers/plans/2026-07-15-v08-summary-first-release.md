# v0.8 Summary-First Loading Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Release an opt-in, summary-first on-demand loading contract that lets compatible agents answer from a short reviewed summary when sufficient and fall back to the full active file when it is not.

**Architecture:** Persistent Memory remains an instruction-only, local-Markdown skill. `SKILL.md` and `SKILL_zh.md` define the agent behavior; both README files explain the optional file format and legacy fallback; `tests/skill-contract.test.mjs` protects the public contract. The prototype fixtures and two-agent result are evidence for this scope, not a runtime dependency.

**Tech Stack:** Markdown, Node.js built-in `node:test`, Git.

## Global Constraints

- Implement only in `C:\Users\Yui\.agents\skills\persistent-memory\.worktrees\v08-summary-first-prototype` on branch `codex/v08-summary-first-prototype`.
- Do not read, copy, modify, migrate, or summarize files under `C:\Users\Yui\.persistent-memory` during implementation or tests.
- Summary-first applies only to active on-demand files selected through `_index.md`; `_core/`, `_index.md`, `_archive/`, `_archive/_index.md`, and `_archive/_trash/` keep their v0.7.1 behavior.
- A summary is optional. Its exact heading is `## Summary` or `## 摘要`, placed after a file title and any introductory metadata, with three to six factual bullet points.
- If the selected active file has no valid summary, read the full file using the existing v0.7.1 behavior; do not error, create a summary automatically, or claim a migration occurred.
- If a summary cannot answer the request, state that the summary is insufficient and read the full file before answering. Do not invent missing details.
- A confirmed update that changes a fact represented in a summary must propose the summary edit in the same preview and wait for the same explicit user confirmation.
- Do not add vector search, databases, knowledge graphs, automatic bulk migration, automatic summary creation, token-savings guarantees, or section-level loading.
- Do not state that v0.8 is released until the implementation, verification, version tag, GitHub Release, and ClawHub update have all completed.

---

## File Structure

- Modify: `SKILL.md` — English runtime contract for optional summary-first on-demand loading and reviewed summary maintenance.
- Modify: `SKILL_zh.md` — Chinese mirror of the same runtime contract.
- Modify: `README.md` — English user explanation, summary format, compatibility fallback, and v0.8 release status.
- Modify: `README_zh.md` — Chinese mirror of the same user explanation and status.
- Modify: `CHANGELOG.md` — add v0.8.0 release notes only after the contract and tests pass.
- Modify: `tests/skill-contract.test.mjs` — replace the v0.7.1 absence assertion with v0.8 positive behavior assertions.
- Keep unchanged: `tests/fixtures/v08-summary-first/`, `tests/v08-summary-first-fixtures.test.mjs`, `docs/experiments/v08-summary-first-prototype.md`, and `docs/experiments/v08-summary-first-results.md`.

### Task 1: Replace the obsolete absence assertion with v0.8 contract tests

**Files:**
- Modify: `tests/skill-contract.test.mjs`
- Test: `tests/skill-contract.test.mjs`

**Interfaces:**
- Consumes: `SKILL.md`, `SKILL_zh.md`, `README.md`, and `README_zh.md` as UTF-8 text.
- Produces: a contract test that fails until both languages document optional `## Summary` / `## 摘要`, legacy full-file fallback, insufficiency escalation, and reviewed summary maintenance.

- [ ] **Step 1: Replace the current v0.7.1 absence test with this failing test**

Replace `test('does not present Summary-first loading as a current feature', ...)` with:

```js
test('documents optional summary-first loading with a safe legacy fallback', async () => {
  const [en, zh, readmeEn, readmeZh] = await Promise.all([
    read('SKILL.md'),
    read('SKILL_zh.md'),
    read('README.md'),
    read('README_zh.md'),
  ]);

  assert.match(en, /Summary-first on-demand loading/i);
  assert.match(en, /## Summary/);
  assert.match(en, /summary is insufficient/i);
  assert.match(en, /no valid summary.*read the full file/is);
  assert.match(zh, /摘要优先的按需加载/);
  assert.match(zh, /## 摘要/);
  assert.match(zh, /摘要不足/);
  assert.match(zh, /没有有效摘要.*读取全文/is);
  assert.match(readmeEn, /optional.*Summary-first/i);
  assert.match(readmeZh, /可选.*摘要优先/);
});

test('requires reviewed summary maintenance without automatic migration', async () => {
  const [en, zh] = await Promise.all([read('SKILL.md'), read('SKILL_zh.md')]);

  assert.match(en, /same preview.*explicit user confirmation/is);
  assert.match(en, /do not automatically create.*Summary/is);
  assert.match(en, /Do not bulk-migrate/i);
  assert.match(zh, /同一次预览.*用户明确确认/is);
  assert.match(zh, /不得自动创建.*摘要/is);
  assert.match(zh, /不得批量迁移/);
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```powershell
node --test tests/skill-contract.test.mjs
```

Expected: FAIL because v0.7.1 explicitly says summary-first loading is not a current feature and does not yet document the new contract.

### Task 2: Implement the bilingual agent behavior contract

**Files:**
- Modify: `SKILL.md`
- Modify: `SKILL_zh.md`
- Test: `tests/skill-contract.test.mjs`

**Interfaces:**
- Consumes: an active on-demand file matched from `_index.md`.
- Produces: either a sufficient answer from an optional summary or a clearly disclosed escalation to the existing full-file read.

- [ ] **Step 1: Replace the v0.7.1 version note in both skill files**

Use these exact notes:

```markdown
**v0.8.0:** This release adds optional Summary-first loading for active on-demand files. It does not add section-level loading, automatic summary creation, or bulk migration.
```

```markdown
**v0.8.0：** 本版为活跃按需文件新增可选的摘要优先加载；不包含 section 级加载、自动创建摘要或批量迁移。
```

- [ ] **Step 2: Replace `Load On Demand` / `按需加载` with equivalent rules**

The English subsection must include this behavior:

```markdown
### Summary-first on-demand loading

For an active on-demand file selected through `_index.md`:

1. If the file has `## Summary` or `## 摘要` immediately after its title and optional introductory metadata, read that summary first. It must contain three to six factual bullet points about current status, key decisions, results, or constraints.
2. If the summary is sufficient for the user's request, answer from it without claiming to have read the full file.
3. If the requested fact is absent, ambiguous, or needs exact supporting detail, say that the summary is insufficient and read the full file before answering. Do not invent the missing detail.
4. If the file has no valid summary, use the existing full-file read behavior. Do not fail, create a summary automatically, or treat the file as migrated.
5. This flow never applies to `_core/`, `_index.md`, or `_archive/`. It is not section-level loading.
```

Add an equivalent Chinese subsection named `### 摘要优先的按需加载`, using the exact phrases asserted by Task 1.

- [ ] **Step 3: Extend the saving contract in both skill files**

After the existing reviewed-save rule, add equivalent language stating:

```markdown
When a confirmed update to an active on-demand file changes a fact represented in its `## Summary` / `## 摘要`, include the exact summary revision in the same preview and obtain the same explicit user confirmation before writing. Do not automatically create a Summary for an existing file and do not bulk-migrate memory files.
```

The Chinese mirror must contain `同一次预览` and `用户明确确认`, and it must explicitly prohibit automatic summary creation and bulk migration.

- [ ] **Step 4: Run the contract test to verify it passes**

Run:

```powershell
node --test tests/skill-contract.test.mjs
```

Expected: PASS for all existing lifecycle tests plus the two new summary-first tests.

### Task 3: Document the optional file format and v0.8 boundary

**Files:**
- Modify: `README.md`
- Modify: `README_zh.md`
- Modify: `CHANGELOG.md`
- Test: `tests/skill-contract.test.mjs`

**Interfaces:**
- Consumes: the agent behavior contract from Task 2.
- Produces: public documentation that tells users what the feature does, how legacy files behave, and what v0.8 does not promise.

- [ ] **Step 1: Add one capability bullet to both README files**

Add after the existing on-demand-detail bullet:

```markdown
- **Uses optional Summary-first loading** — for an active file with a reviewed `## Summary`, the agent reads the short summary first and opens the full file only when the request needs more detail. Files without a summary keep the existing behavior.
```

```markdown
- **可选摘要优先加载**：活跃文件含有经审核的 `## 摘要` 时，agent 先读短摘要；只有问题需要更多细节才读取全文。没有摘要的文件保持原有行为。
```

- [ ] **Step 2: Add a `## Summary-first files` / `## 摘要优先文件` section**

Document the exact optional schema:

```markdown
# Project title

> Optional introductory metadata

## Summary

- Current status or scope
- Key decision or result
- Important constraint or uncertainty

## Full Details
```

Explain in both languages that `## Summary` and `## 摘要` are accepted; summaries contain three to six factual bullets; the agent says when the summary is insufficient; users are not asked to bulk-migrate old files; and a reviewed update changes the summary together with the affected body fact.

- [ ] **Step 3: Replace the v0.7.1 release-status sentence**

Use these exact lines:

```markdown
v0.8.0 adds optional Summary-first loading for active on-demand files. It does not add section-level loading, automatic summary creation, or bulk migration. See [CHANGELOG.md](CHANGELOG.md) for release details.
```

```markdown
v0.8.0 为活跃按需文件新增可选摘要优先加载；不包含 section 级加载、自动创建摘要或批量迁移。版本详情见 [CHANGELOG.md](CHANGELOG.md)。
```

- [ ] **Step 4: Add the v0.8.0 changelog section above v0.7.1**

```markdown
## v0.8.0 — 2026-07-15

- Added optional Summary-first loading for active on-demand memory files.
- Preserved full-file loading for legacy files without a valid Summary.
- Required reviewed summary updates whenever a confirmed body change affects a summarized fact.
- Kept `_core/`, indexes, and archives outside the feature scope.
- Kept section-level loading, automatic summary creation, and bulk migration out of scope.
```

- [ ] **Step 5: Run the full automated suite**

Run:

```powershell
node --test tests/skill-contract.test.mjs tests/v08-summary-first-fixtures.test.mjs
```

Expected: 13 tests pass, 0 failures.

### Task 4: Verify the release contract and prepare the versioned handoff

**Files:**
- Test: `SKILL.md`, `SKILL_zh.md`, `README.md`, `README_zh.md`, `CHANGELOG.md`, and `tests/skill-contract.test.mjs`

**Interfaces:**
- Consumes: the v0.8 documentation contract and the existing synthetic prototype fixtures.
- Produces: a clean, versioned v0.8 implementation commit ready for a user-approved tag, GitHub Release, and ClawHub update.

- [ ] **Step 1: Run the synthetic acceptance scenarios**

Review these three scenarios against both skill files:

1. An active indexed file has `## 摘要`; a question about its listed status must be answered from the summary without claiming the full file was read.
2. The same file is asked for a detail absent from the summary; the response must say `摘要不足` / `summary is insufficient` before reading the full file.
3. An old active file has no summary; the response must read the full file without creating a summary or calling the file migrated.

Record pass/fail in the implementation handoff.

- [ ] **Step 2: Run final static checks**

Run:

```powershell
node --test tests/skill-contract.test.mjs tests/v08-summary-first-fixtures.test.mjs
git diff --check
git status --short
```

Expected: 13 tests pass, `git diff --check` has no output, and only the six v0.8 contract files plus this plan are changed.

- [ ] **Step 3: Commit the implementation**

Run:

```powershell
git add SKILL.md SKILL_zh.md README.md README_zh.md CHANGELOG.md tests/skill-contract.test.mjs docs/superpowers/plans/2026-07-15-v08-summary-first-release.md
git commit -m "feat: add summary-first loading"
```

Expected: one versioned implementation commit on `codex/v08-summary-first-prototype`.

- [ ] **Step 4: Request release authorization after the commit**

Before any external publication, present the verified commit, test result, and exact public actions: create Git tag `v0.8.0`, create the matching GitHub Release, and publish an update to the existing ClawHub `persistent-memory-skill` listing. Wait for explicit user confirmation before each external publication action.

## Self-Review

- Scope coverage: Task 1 makes the v0.8 promise executable; Task 2 defines exactly when an agent reads a summary, escalates, falls back, and updates a reviewed summary; Task 3 makes the same behavior visible to users; Task 4 verifies and commits the contract without publishing it prematurely.
- User-memory protection: Every implementation task operates only in the repository worktree. The global constraints forbid reading, copying, editing, or bulk-migrating the user memory root.
- Product boundary: The contract explicitly preserves legacy behavior and excludes section-level loading, automatic summary generation, bulk migration, vector search, databases, and knowledge graphs.
- Placeholder scan: Every changed file, test assertion, command, public claim, and release gate is specified.
