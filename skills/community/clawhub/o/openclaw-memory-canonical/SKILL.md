---
name: openclaw-memory-canonical
description: >
  Lightweight file-based memory system for single-user AI agents. Uses markdown files only: HOT/WARM/COLD/BUFFER plus SCRATCH learnings,
  with tiered loading, WAL-lite writes, compaction recovery, weekly review, TTL archival, health checks, and a built-in self-improvement loop.
  Use when setting up or improving agent memory, preventing memory bloat or repeated mistakes, promoting recurring lessons into durable files,
  validating memory health, or when users mention memory systems, working buffers, episodic/semantic/procedural memory, learnings, weekly review,
  self-improvement, or how an AI agent should remember and improve between sessions.
---

# OpenClaw Memory v4.6.14 (2026-04-14)

File-based memory system for single-user AI agents: HOT/WARM/COLD/BUFFER + SCRATCH. Small, grep-first, zero external service dependencies (assumes standard Unix tools).

## Execution

### Path Convention
Run runtime commands from the workspace root so both `memory/` and `skills/` paths resolve correctly.
In a real workspace, runtime scripts live under `memory/scripts/`. Never use `bash scripts/`. Always prefix with `memory/`.

This skill package also ships reference scripts under `skills/openclaw-memory-canonical/scripts/` for review, copying, and local testing. The bundled scripts resolve the workspace root dynamically so they can be tested from the skill folder before being copied into `memory/scripts/`.

### Installed Runtime vs Packaged Skill
Treat `skills/openclaw-memory-canonical/` and `memory/scripts/` as two distinct surfaces:
- `skills/openclaw-memory-canonical/` = packaged reference version of the skill
- `memory/scripts/` = deployed runtime scripts actually used by the workspace

A ClawHub install or update refreshes the packaged skill tree, but it does **not** automatically overwrite already-deployed `memory/scripts/` files.
After every install or update of this skill, explicitly re-sync the deployed runtime scripts before trusting runtime behavior changes:

```bash
mkdir -p memory/scripts
cp skills/openclaw-memory-canonical/scripts/*.sh memory/scripts/
chmod +x memory/scripts/*.sh
bash memory/scripts/health-check.sh
```

Until that re-sync + validation step is complete, trust `memory/scripts/` for actual file operations and host-side runtime behavior, but treat this skill's Markdown instructions (Runtime Decision Tree, Mechanisms, thresholds, and routing rules) as immediately authoritative for AI planning and decision logic. A ClawHub update alone is not enough to claim deployed runtime tool behavior changed.

If you need to compare packaged vs deployed runtime before overwriting, diff them first:

```bash
diff -u skills/openclaw-memory-canonical/scripts/health-check.sh memory/scripts/health-check.sh || true
```

If the packaged scripts changed but `memory/scripts/` was not re-synced yet, trust the deployed runtime behavior until re-sync + validation are complete.

### Execution Hierarchy
1. Follow `Runtime Decision Tree` first for the active session.
2. Use `Mechanisms` next for implementation rules.
3. Use `Core Design & Tables` for routing and structure.
4. Use `References` last for rationale, edge cases, and script internals.
If text disagrees, follow #1. Do not scan backward.

### Runtime Decision Tree (for AI execution)

**On session start:**
1. If `MEMORY.md` does not exist, create it with the canonical 4-line header before proceeding.
2. Read `MEMORY.md`.
3. If `memory/scripts/` does not exist or is missing `.sh` files, bootstrap them explicitly: `mkdir -p memory/scripts && cp skills/openclaw-memory-canonical/scripts/*.sh memory/scripts/ && chmod +x memory/scripts/*.sh`.
   - After any future skill install or update, re-run this sync step explicitly before assuming deployed runtime scripts picked up the packaged changes.
   - Validation rule: after re-sync, run `bash memory/scripts/health-check.sh` before relying on the updated runtime contract.
   - If a required `bash memory/scripts/health-check.sh` preflight cannot run because the script is missing or not executable, do not substitute an informal manual pass/fail judgment. First bootstrap or re-sync `memory/scripts/` from `skills/openclaw-memory-canonical/scripts/`, then rerun `bash memory/scripts/health-check.sh` and trust that real result.
   - If re-sync has not happened yet after an install or update, do not describe the new packaged behavior as live runtime behavior on this host.
4. If `memory/working-buffer.md` does not exist, create it with the standard working-buffer header and current timestamps before proceeding.
5. Read `memory/working-buffer.md`. Immediately update its `last_active:` line to the current ISO-8601 timestamp.
6. Clear stale locks, then handle `memory/working-buffer.md.pending`:
   - If `memory/working-buffer.md.lock` exists, delete it unconditionally.
   - If `.pending` does not exist, go to step 7.
   - If `.pending` exists:
     1. Read `.pending`.
     2. Recovery fails only if the file is empty, whitespace-only, or does not start with exactly this 4-line working-buffer header in order: line 1 `# Working Buffer`; line 2 `created: ` followed by a valid ISO-8601 timestamp; line 3 `last_active: ` followed by a valid ISO-8601 timestamp; line 4 blank. Any deviation in field names, order, timestamp validity, or the required blank line fails recovery; otherwise continue to the recovery action.
     3. If recovery fails, log one concise line to `.learnings/ERRORS.md`, notify the user, discard `.pending`, overwrite `memory/working-buffer.md` with a fresh header, and go to step 7.
     4. If recovery succeeds, restore `memory/working-buffer.md` from `.pending`, then discard `.pending`.
     5. Active task lines are bullet-list lines starting with `- ` after `## Active Task:` that contain non-whitespace content.
     6. If the recovered buffer is stale (`last_active` is more than 2 hours old) or there are no active task lines, append its body (skip the 4-line header) to today's episodic file with a `[RECOVERED: STALE]` marker, ensuring the 4-line closure block remains the absolute final lines of the episodic file, then overwrite `memory/working-buffer.md` with a fresh header.
     7. If the recovered buffer is not stale, still has active task lines, and already exceeds the runtime threshold (>3 active subtasks or >80 lines), immediately run the Buffer Rotation Procedure (steps 1-5) before continuing, then proceed with a fresh working buffer.
     8. Otherwise keep the recovered buffer and continue.
7. If `.pending` did not exist and `memory/working-buffer.md` `last_active` is more than 2 hours old, append its body (skip the 4-line header) to today's episodic file with a `[RECOVERED: STALE]` marker, ensuring the 4-line closure block remains the absolute final lines of the episodic file, then overwrite `memory/working-buffer.md` with a fresh header.
8. Read episodic notes for today and yesterday, then continue with the recent-context scan.
9. Scan the last 20 lines of `.learnings/ERRORS.md`, `.learnings/LEARNINGS.md`, and `.learnings/FEATURE_REQUESTS.md` if those files exist. Stop after either: (a) applying one relevant lesson that matches the current task, or (b) scanning all three files once. If nothing relevant exists, emit nothing.
10. Steps 1-9 define the mandatory base context. For any additional memory needed beyond this base, use targeted `grep` searches on demand. Do not proactively load other memory files. If a targeted `grep` returns zero matches, stop searching and proceed with the available context.

**At session end:**
1. If `memory/working-buffer.md` contains active task lines (bullet-list lines starting with `- ` after `## Active Task:` that contain non-whitespace content), run the Buffer Rotation Procedure, then finish session cleanup. Skip the health-check pre-flight here, because rotation is the designated remediation for the buffer-length invariant.
2. If the buffer has only the header and no active task lines, stop session cleanup with no rotation.
3. Do not rotate mid-task unless the user explicitly requests it; otherwise continue active work.

**Before lesson promotion or `MEMORY.md` rewrite (pre-commit gate):**
1. Run `bash memory/scripts/health-check.sh`. If it FAILs, fix the reported invariant before continuing.
2. Re-scan `.learnings/*` only if one of these is true:
   - the user goal changed to a distinct task
   - the work switched from read-only analysis to write/repair work
   - a prior attempt already failed
   - the user explicitly asked to re-scan learnings
3. Do not re-scan for small follow-up questions, clarifications, or minor edits on the same artifact; otherwise continue with the current context.
4. If a prior lesson clearly matches the current task, apply it, then continue with the adjusted plan.
5. If nothing matches, continue silently. Stop after either applying one relevant lesson or confirming that nothing relevant matched.

**Before writing any important fact:**
- Write the fact to `memory/working-buffer.md` first.
- Then reply or continue the task.

**After a failure, correction, or missing capability:**
- Log one concise line in the matching `.learnings/` file.
- If the lesson is broadly reusable, promote it to the right durable file.
- Do not log `nothing found` or other no-op activity.

**When `working-buffer.md` grows too large mid-session:**
- Threshold: more than 3 active bullet lines under `## Active Task:` OR more than 80 lines.
- Check the counts with `grep -c '^-[[:space:]]' memory/working-buffer.md` and `wc -l memory/working-buffer.md` instead of estimating manually.
- Action: defer rotation until session end. Continue working. Do not rotate mid-task.
- Clarification: this mid-session deferral rule applies only to buffer growth that occurs after session-start recovery. It does not override the immediate-rotation path for an already-oversized buffer recovered at session start (Runtime Decision Tree step 6.7).
- Exception: if weekly review runs, ABORT review and append `Buffer oversized; deferring weekly review until session-end rotation` to today's episodic note. Do not interrupt active work.

**If `health-check.sh` fails:**
- Stop memory-dependent reasoning.
- Tell the user: `Memory integrity check failed. Run bash memory/scripts/health-check.sh`.
- You may still greet, clarify the current request, explain what memory is broken, or help fix the failing check.
- Do not answer questions that require retrieving semantic memory, procedural memory, or older episodic facts until the check is fixed.

**When searching memory:**
- HOT → `MEMORY.md` is always in context.
- WARM → search `memory/semantic/` and `memory/procedural/` first.
- COLD → search `memory/episodic/` only when needed.

## Core Design

3 types, 4 primary tiers + SCRATCH, 10 mechanisms that fit in a terminal.

### 3 Types

| Type | What | Lives |
|------|------|-------|
| **Episodic** | What happened | `memory/episodic/YYYY-MM-DD.md` |
| **Semantic** | What I know | `memory/semantic/*.md` |
| **Procedural** | How to do things | `memory/procedural/*.md` |

### 4 Primary Tiers + SCRATCH

| Tier | Files | When to load |
|------|-------|-------------|
| **HOT** | `MEMORY.md` (≤60 lines) | Every session |
| **WARM** | `semantic/*.md`, `procedural/*.md` | By context (grep tags + metadata freshness) |
| **COLD** | `episodic/`, `archive/` | On query |
| **BUFFER** | `working-buffer.md` | During active task |
| **SCRATCH** | `.learnings/*.md` | Session start (scan recent relevant lines) |

### Directory Structure

```
MEMORY.md                          ← HOT, ≤60 lines, always loaded
├── .learnings/                    ← SCRATCH, recent failures/corrections/capability gaps
│   ├── ERRORS.md
│   ├── LEARNINGS.md
│   └── FEATURE_REQUESTS.md
├── memory/
│   ├── episodic/                  ← COLD, one per day
│   │   └── YYYY-MM-DD.md          ← events, decisions, signals
│   ├── semantic/                  ← WARM, one per domain
│   │   ├── infrastructure.md      ← IP, ports, services
│   │   ├── preferences.md         ← style, rules, habits
│   │   ├── projects.md            ← active projects
│   │   └── decisions.md           ← final decisions with why
│   ├── procedural/                ← WARM, how-to + lessons
│   │   ├── lessons-learned.md     ← post-mortems, anti-patterns
│   │   └── (other how-to files)
│   ├── working-buffer.md          ← BUFFER, active task scratchpad
│   ├── archive/YYYY/MM/           ← episodic >30 days, auto-moved
│   ├── archive/learnings/YYYY/MM/ ← SCRATCH entries >30 days without promotion
│   └── scripts/
│       ├── archive-old-episodic.sh ← episodic TTL archiver
│       ├── archive-old-learnings.sh← legacy SCRATCH TTL archiver
│       ├── atomic-write.sh         ← crash-safe file writes
│       └── health-check.sh         ← invariant validation
```

### MEMORY.md Header (≤60 lines total)

```markdown
# Agent Memory
#tags: <frozen-vocabulary>
last_verified: YYYY-MM-DD
last_updated: YYYY-MM-DD
```

Only these 4 lines are mandatory. Header validation is exact: line 1 MUST be `# Agent Memory`; line 2 MUST start with `#tags:` followed by frozen-vocabulary tags; lines 3-4 MUST be `last_verified:` and `last_updated:` with ISO dates. The body contains ≤56 lines of durable context. Never exceed 60 lines total.

### WARM File Header (freshness metadata)

Every file in `memory/semantic/*.md` and `memory/procedural/*.md` should include this minimal header shape:

```markdown
# <title>
#tags: <frozen-vocabulary>
> last_verified: YYYY-MM-DD
```

The leading `>` blockquote marker on `last_verified` is the documented reference format. The shipped `health-check.sh` also accepts plain `last_verified:` for backward compatibility. If you intentionally remove that compatibility path later, update the script and this skill text together in the same change.

## Mechanisms

### 1. Buffer-first writes

Before answering with important info (decisions, corrections, facts), write to `working-buffer.md` first. Then reply. Files survive restarts.

**Working buffer header format (v4.1+):**
```markdown
# Working Buffer
created: 2026-04-05T14:31:00+08:00
last_active: 2026-04-05T14:31:00+08:00

## Active Task:
- ...
```

Header enables:
- **Stale detection:** If `last_active` > 2 hours and no current session working on it → abandoned buffer
- **Maintenance:** Always update `last_active` to the current ISO timestamp on every buffer append or session resume
- **Compaction recovery:** Distinguish current task from leftover buffer

**Heartbeat invariant:** After loading or modifying `memory/working-buffer.md`, immediately update the `last_active:` line to the current ISO-8601 timestamp. Do not treat it as static metadata. The 2-hour stale checks and weekly-review session gate depend on this heartbeat.

**How to update `last_active` safely:** Use an in-place line replacement and verify the result:
```bash
sed -i "s/^last_active:.*/last_active: $(date -Iseconds)/" memory/working-buffer.md
grep '^last_active:' memory/working-buffer.md
```
If `sed -i` is unavailable or you prefer a full rewrite, use `atomic-write.sh` with the complete updated file content.

### 2. Canonical Owner Rule — Principle, Not Mechanism

This is a design rule, not a runtime branch table. Use it to decide where a fact belongs. Do not treat it as a step-by-step workflow. When a fact could plausibly fit multiple homes, choose the most specific home based on its primary nature; if it is still ambiguous, default to today's episodic note and add a `#routing-note:` that explains the ambiguity for weekly review.

Each class of fact has exactly one home. Never duplicate:

| Fact type | Lives in |
|-----------|----------|
| IP, ports, services | `semantic/infrastructure.md` |
| Preferences, style, rules | `semantic/preferences.md` |
| Commands, how-to | `procedural/*.md` |
| Events, decisions, timeline | `episodic/YYYY-MM-DD.md` |
| Post-mortems, anti-patterns | `procedural/lessons-learned.md` |
| Final decisions with rationale | `semantic/decisions.md` |

### 3. Atomic Writes

Prevent corrupted files on crash. Prefer the bundled script:

```bash
echo "content" | bash memory/scripts/atomic-write.sh /path/to/file.md
```

Rule: write the complete temp file first. Replace the target file only after the temp file is complete. See references for full fallback details.

### 4. Closure Blocks in Episodic

End every episodic note with 4 lines:

```
Updated: YYYY-MM-DD
Decisions: what was changed
Signal: what I learned about the system
Open: remaining items (or "none")
```

Decision = what I changed. Signal = what I learned.

### 5. Episodic TTL

Archive files older than N days into `archive/YYYY/MM/`:

```bash
bash memory/scripts/archive-old-episodic.sh 30   # default 30
```

### 5b. SCRATCH TTL (`.learnings/`)

Auto-archive only legacy or non-canonical scratch note files older than 30 days:
- last-modified >30 days → move to `memory/archive/learnings/YYYY/MM/`
- never delete permanently (`trash` > `rm`)
- files containing a line that ends with `#pinned` are exempt until manually unpinned
- keep the active SCRATCH surface canonical and in place: `ERRORS.md`, `LEARNINGS.md`, `FEATURE_REQUESTS.md`
- use `bash memory/scripts/archive-old-learnings.sh 30` for the legacy/non-canonical archival pass
- line-level pruning inside the canonical SCRATCH files is manual review work, not automatic TTL behavior

### 6. Buffer Rotation Procedure (run only when triggered by the runtime decision tree or at session end)

1. If `working-buffer.md.lock` exists, abort rotation. Recovery first.
2. Write `working-buffer.md.lock`.
3. Append the buffer body (skip the exact 4-line header: `# Working Buffer`, `created: ...`, `last_active: ...`, blank line) to today's episodic note without displacing the closure block.
   - If today's episodic file already ends with a valid 4-line closure block, insert the appended body before those final 4 lines, then verify the closure block still terminates the file with a deterministic terminal check such as `tail -n 1 memory/episodic/YYYY-MM-DD.md | grep -q '^Open:'`.
   - If that terminal assertion fails, rebuild the file deterministically with `atomic-write.sh`: reassemble (a) the pre-closure body of today's episodic file, (b) the appended working-buffer body, and (c) the original 4-line closure block, in that order, then write the rebuilt full file atomically before continuing.
   - If today's episodic file does not yet end with a valid closure block, append the working-buffer body and then write a fresh 4-line closure block before continuing.
4. Overwrite `memory/working-buffer.md` with a fresh header.
5. Remove `memory/working-buffer.md.lock` unconditionally.

Use `wc -l memory/working-buffer.md` when you need a deterministic line count before deciding whether rotation is required.

**Recovery:** If `working-buffer.md.pending` exists, recover it before any other operation. If `working-buffer.md.lock` exists at session start, delete it unconditionally before proceeding with `.pending` recovery or staleness evaluation.

### 7. Weekly Review (cron, Monday 9:00)

**Trigger contract:** weekly review is a semi-autonomous maintenance flow scheduled for Monday 9:00. A human may also invoke the same checklist manually when needed. It performs deterministic maintenance automatically but requires manual confirmation for promotions. Treat both paths as the same review procedure; the cron schedule is the default trigger, not a separate behavior.

**Minimal safe v1 weekly review** should automate only deterministic maintenance plus candidate detection.

Checklist (run at the scheduled Monday 9:00 review or when manually prompted):
1. If `working-buffer.md.lock` exists, delete it unconditionally before evaluating the session gate.
2. Session gate: if `working-buffer.md` has `last_active` less than 2 hours ago, skip/defer review, log `Active session detected`, and stop
3. Size gate: if the buffer has more than 3 active subtasks OR more than 80 lines, abort review, log `Buffer oversized`, and stop until rotation happens first
4. Run `memory/scripts/health-check.sh`; if the script is missing or not executable, first bootstrap/re-sync `memory/scripts/` from `skills/openclaw-memory-canonical/scripts/`, then rerun `bash memory/scripts/health-check.sh`. If the rerun FAILs, stop review and fix health first.
5. Run episodic archival (>30 days): `bash memory/scripts/archive-old-episodic.sh 30`
6. Run legacy `.learnings/` archival (>30 days): `bash memory/scripts/archive-old-learnings.sh 30`
7. Recurrence check: flag any lesson line appearing ≥3 times across `.learnings/ERRORS.md` and `.learnings/LEARNINGS.md` as `[PROMOTE-CANDIDATE]`. Normalize by lowercasing and collapsing whitespace before comparing. If no helper script automates this check, skip this step entirely; do not attempt manual line-by-line comparison.
8. Ensure today's episodic file terminates with exactly one 4-line closure block containing these fields: `Updated: YYYY-MM-DD`, `Decisions: weekly review performed` (or the real maintenance action), `Signal: <what the review learned>`, `Open: none` (or the real remaining item). If a valid closure block already exists at the file end, overwrite those final 4 lines in place with the weekly-review state; otherwise append a fresh 4-line closure block.

Do **not** do these automatically in v1:
- semantic extraction from episodic notes beyond counting repeated lesson patterns
- lesson promotion into semantic/procedural memory
- `last_verified` refresh
- `MEMORY.md` rewrite
- forced working-buffer rotation during review

If nothing meaningful changed → skip with "No meaningful changes".

### 8. Health Check (invariant validation)

Before lesson promotion or `MEMORY.md` rewrite, run:

```bash
bash memory/scripts/health-check.sh
```

If the script is missing or not executable, first bootstrap/re-sync `memory/scripts/` from `skills/openclaw-memory-canonical/scripts/`, then rerun `bash memory/scripts/health-check.sh` before proceeding.

Health check should cover at least: `MEMORY.md` header validity, tags on line 2, frozen vocabulary, WARM-file `> last_verified:` freshness, exact working-buffer 4-line header validity (`# Working Buffer`, `created:`, `last_active:`, blank line), buffer <80 lines, closure blocks, and pending/rotating files absent.
Returns exit code 0 if all required checks pass, 1 if any fail.

Treat `health-check.sh` as a separate script in the reference implementation, not as implicit model behavior.

If `health-check.sh` fails:
- Do not auto-fix memory unless the user explicitly asked you to repair it.
- Output the exact failure message.
- You may explain the failure and suggest a safe next command.
- If the user explicitly asked for repair, fix only the reported invariant and then re-run `bash memory/scripts/health-check.sh`.
- If the failure output is unclear, run `bash memory/scripts/health-check.sh --verbose` before making changes.

Buffer rotation is exempt from this pre-flight check, because buffer rotation is the designated remediation for the buffer-length invariant.

### 9. Grep-Based Tag Discovery

Example of a relevant lesson match: if the current task is fixing a Docker build and `.learnings/ERRORS.md` contains a lesson about a Docker build flag that fixes the same failure mode, apply it. If the lesson is unrelated to the current task, ignore it.

Every WARM file has `#tags:` on line 2:

```bash
grep -rl "qdrant" memory/                         # all files mentioning qdrant
grep -rl "#tags:.*networking" memory/              # files tagged networking
head -2 memory/**/*.md | grep "#tags:"             # discover all tags
```

### 10. Self-Improvement Loop

Capture only lessons that should change future behavior.

**Write immediately after:**
- a command fails
- a user corrects the agent
- a capability is missing
- an external tool or API fails
- knowledge is outdated
- a better recurring approach is discovered

**Use these files:**
- `.learnings/ERRORS.md` → what failed, why, and the fix attempt
- `.learnings/LEARNINGS.md` → what was wrong and the better way
- `.learnings/FEATURE_REQUESTS.md` → the missing capability, impact, and desired behavior

**Promotion workflow (zero auto-promotion):**

1. Flag as `[PROMOTE-CANDIDATE]` when one of these is true:
   - the user explicitly says `remember this`, `make this permanent`, `make permanent`, or `add to knowledge`
   - the lesson prevents data loss, a security issue, or an unrecoverable error
   - the same pattern recurs 3 or more times
2. Promote to durable memory only after explicit user approval or manual weekly review confirmation.
3. If nothing meets the criteria, keep it in `.learnings/`.

**Target mapping for promotion:**
- command syntax, debugging steps, repeatable fixes →
  - if the lesson fits an existing procedural file, append there
  - otherwise create `memory/procedural/<topic>.md` only after 3 or more promotions on the same topic
- infrastructure facts, preferences, durable facts → `memory/semantic/*.md`
- anti-patterns and post-mortems → `memory/procedural/lessons-learned.md` (always, not generic procedural)
- decisions with rationale → `memory/semantic/decisions.md`

**Do not promote:**
- one-off fixes
- session-specific context
- preferences that matter only for today

## Tag Vocabulary (Frozen)

**infrastructure:** tailscale, tailnet, docker, synapse, matrix, coturn, qdrant, ubuntu, systemd, ufw, fail2ban, samba, ssh, networking, gateway, pm2
**preferences:** rules, style, workflow, memory, habits
**projects:** audit, skills, security, review
**procedural:** deepseek, puppeteer, benchmark, troubleshooting, tasks, checklist, backup, diagnostics
**lessons:** postmortem, errors, fixes, anti-patterns

Do not invent new tags.

## Friction Log

If a task takes >5 minutes of waiting/googling → note it inline with `#friction:` tag in the working buffer. Weekly review may record that friction exists, but in the minimal safe v1 it should not auto-promote friction into `lessons-learned.md` without manual review.

## Known Limits (documented, not fixed)

- **No file locking for concurrent writes** — Single writer assumed; stagger crons to avoid overlap between cron jobs and main session
- **No auto-promotion**: Important signals in old episodic files don't auto-surface to semantic; relies on weekly review to surface candidates, not to promote automatically
- **Tag enforcement is reactive**: `health-check.sh` validates tags against the frozen vocabulary after writes, but it does not prevent a bad tag from being written in the first place
- **Frozen vocabulary requires synchronized updates**: if you intentionally change the frozen tag list, update both the skill text and `health-check.sh`
- **WARM freshness format is documented + backward-compatible today**: the reference format is `> last_verified:`, while `health-check.sh` also accepts plain `last_verified:` to avoid breaking older files
- **GNU date parsing is assumed**: `health-check.sh` currently uses `date -d`, so non-GNU environments may need a synchronized portability patch before relying on the script as-is
- **Weekly review is intentionally minimal**: it performs deterministic maintenance, not semantic judgment

## Hard Constraints

- Write the same fact to exactly one file (see Canonical Owner Rule).
- Never delete files: use `trash` or `archive/`. Never `rm`.
- Never store credentials in episodic notes.
- Never invent tags outside the frozen vocabulary.
- Never duplicate lessons across `.learnings/` files.
- Do not log `nothing found`, `no-op`, or scan metadata.
- Use shell commands such as `wc -l` for line-count checks instead of manual estimates when a threshold matters.
- After every structural update, write the changed file to disk immediately (prefer `atomic-write.sh` for full-file rewrites).

## Why This Works

- **Text > brain**: Files survive restarts. Mental notes don't.
- **Grep > database**: No vector DB, no API, no dependency chain.
- **Small context**: 60-line MEMORY.md fits in any prompt.
- **Self-maintaining**: TTL archival + weekly review + health check + buffer rotation.
- **Hard to break**: Atomic writes, canonical owners, frozen tags, invariant checks.
- **Reality-tested**: validation drill catches integration failures before they become memory corruption.

### Post-Patch Validation for Publish Scope
When the asked scope includes packaging or publication, complete all accepted version-metadata, documentation, and release-evidence updates that belong inside the hashed package tree first, then run one deterministic package-validation pass after the final accepted patch:

```bash
cd skills/openclaw-memory-canonical
find . -type f \
  -not -path './.clawhub/*' \
  -not -path './.logs/*' \
  -not -path './.sessions/*' \
  -not -path './.profile/*' \
  -not -path './node_modules/*' \
  -not -path './dist/*' \
  -not -path './references/package-tree.sha256' \
  -not -name '*.tmp' \
  -not -name '*.pending' \
  -not -name '*.lock' \
  | sort | xargs sha256sum > references/package-tree.sha256
```

Record that command and its observed result in `references/verification-evidence.md` and `references/reference-test-log.md` before claiming the artifact is ready to publish.
Chronology rule: finalize every hashed package file first, generate `references/package-tree.sha256` last among in-package content updates, and do not edit any hashed package files after that generation before publish.

See `references/design-rationale.md` for the full decision trail from the 6-round multi-orchestrator pass that shaped the current publish-ready system.
See `UPGRADE.md` for the installed-runtime re-sync contract after ClawHub installs or updates.
See `references/verification-evidence.md`, `references/reference-test-log.md`, and `references/package-tree.sha256` for the current release evidence.
