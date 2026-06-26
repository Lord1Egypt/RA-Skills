---
name: graph-memory-zero
description: Production playbook for OpenClaw graph-memory optimization with mem0-aligned recall governance. Use when users ask to (1) summarize current graph-memory status, (2) reproduce the same optimization effect on another workspace, (3) tune threshold/infer/memoryType/preferenceLexicon for precision vs recall, (4) troubleshoot recall quality drift, or (5) apply/rollback safe config patches under plugins.entries.graph-memory.config.
---

# Graph Memory Zero

## Mission

Deliver a **reproducible** graph-memory optimization outcome (not just a config diff):
- stable recall behavior
- explainable filtering semantics
- safe rollout + rollback
- observable runtime state

If user asks “达到你这套效果”, execute the full playbook below.

## Load order (mandatory)

1. `references/current-baseline.md` (known-good baseline)
2. `references/baseline-profiles.md` (balanced/precision/recall profiles)
3. `references/verification-playbook.md` (acceptance checks)
4. `references/troubleshooting.md` (if any mismatch/failure)

When the user asks about install/download/distribution options, also load:
- `references/install-channels.md`

## Reproducible rollout workflow

### Phase 0 — Snapshot and schema guard

1. Run `gateway.config.schema.lookup` for:
   - `plugins.entries.graph-memory.config`
   - `plugins.entries.graph-memory.config.recallPolicy`
2. Run `gateway.config.get` and store:
   - current config snapshot
   - `baseHash`
3. Report: plugin enabled state, llm/embedding model, recall policy keys present.

Do not patch before confirming schema path exists.

---

### Phase 1 — Normalize semantics (mem0-compatible)

Ensure these compatibility rules are explicitly explained in summary:

- `threshold` is mem0-style alias; legacy `minScore` may still exist.
- If both appear, **effective threshold = max(threshold, minScore)** (stricter wins).
- `infer` is deterministic inference/expansion; no extra LLM call.
- `filters.memoryType` supports `fact|preference|task|event|all`.
- `preferenceLexicon` (versioned) has higher priority than legacy `preferenceKeywords`.

If any rule is not represented in runtime config, patch minimal fields only.

---

### Phase 2 — Apply profile patch (minimal mutation)

Default profile is **balanced** unless user requests otherwise.

Use `gateway.config.patch` with smallest scoped patch under:
- `plugins.entries.graph-memory.config.recallPolicy`

Balanced target (canonical):
- `threshold: 0.62`
- `infer: true`
- `filters.memoryType: all`
- `preferenceLexicon.version: 2026-03-27.balance-v1`
- `preferenceLexicon.enabled: true`
- `preferenceLexicon.keywords`: include EN+ZH preference words

If user asks for stronger precision or stronger recall, choose profile from `references/baseline-profiles.md`.

---

### Phase 3 — Post-restart verification

After patch + restart, verify all below:

1. Effective config re-read matches intended patch.
2. `gm_search` debug details available (`details.debug` includes threshold/infer/filter summary).
3. No schema/key regression (`memoryType` not dropped, lexicon keys intact).
4. Query spot-checks pass (from verification playbook).

If any check fails, enter troubleshooting flow.

---

### Phase 4 — Quality validation (must do before claiming success)

Run the query set in `references/verification-playbook.md` and compare:
- preference-sensitive queries
- task/event retrieval queries
- mixed-language (CN/EN) preference terms

Success criteria (minimum):
- relevant top hits improve or stay stable
- off-topic hits do not increase materially
- preference-related queries show better intent alignment

Do not claim “优化完成” without this phase.

---

### Phase 5 — Rollback safety

Always keep rollback notes in output:

- previous values (`before`)
- target values (`after`)
- one-step revert patch path

If regression is observed, rollback immediately to previous stable profile.

## Failure handling

### A) Local test execution fails

If extension tests fail locally but config intent is clear:
1. Skip blocking local test path.
2. Use controlled `gateway.config.patch` rollout.
3. Run verification playbook.
4. Keep explicit rollback entry.

### B) PowerShell path / command failed

If errors indicate missing path or command failure:
1. Validate path with `Test-Path` first.
2. Confirm script/CLI location and permissions.
3. Retry minimal command only after path is confirmed.

### C) Version mismatch signals

If extension folder version and runtime installed version differ:
- treat as metadata mismatch
- continue config-level rollout, but report mismatch as release check item

## Output contract (default reply structure)

Use this structure for user-facing summary:

1. **当前状态**：enabled / model / embedding / recallPolicy
2. **mem0 对齐语义**：threshold-minScore、infer、memoryType、lexicon
3. **本次变更**：before → after（只列关键键）
4. **验证结果**：通过项 / 风险项 / 观测数据
5. **下一步建议**：继续调优或保持当前
6. **回滚信息**：可直接执行的 revert 说明

Keep answers concise-first, but never omit verification and rollback details.

## Distribution guidance (when requested)

If user asks "how can others install this", provide at least 3 channels:
1. ClawHub registry install (online)
2. Offline package install (`.skill` as zip artifact)
3. Source-folder install (copy skill folder into workspace `skills/`)

Always include:
- required folder layout check (`SKILL.md` at skill root)
- post-install reload step (`openclaw gateway restart`)
- quick verification (`skill appears in available skills and can be triggered`)

## Anti-patterns (forbid)

- Large full-config overwrite when only recallPolicy needs change.
- Declaring success without post-restart validation.
- Ignoring threshold/minScore conflict resolution.
- Omitting lexicon version in production summary.
- Hiding test/verification gaps.
