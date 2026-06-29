# GLIC / UGLIC Check Examples

Real-world examples demonstrating the expected quality and style.

- Example 1 & 3 use generic/hypothetical filenames (e.g. `send_message.py`)
  for teaching the severity logic; the code shown is illustrative.
- Example 2 & 4 reference real open-source skills (`copy-my-profile` and
  `glic-check` itself) — file:line citations there are real and verifiable.

---

## Example 1: Code Check — `send_message.py` card-rendering refactor

Target: `send_message.py` recent changes (card entity creation + broadcast path).
*(Hypothetical code. Citations like `send.py:1204` are illustrative — the severity logic and report shape are what to learn from.)*

### G — Grammar
✅ No issues
- Private function `_get_or_create_card_entity` follows project's underscore-prefix convention
- Constant `CARD_ENTITY_CACHE` is uppercase, consistent with `SEND_LOG_FILE` etc.
- `nonlocal card_schema_str` usage is correct

### L — Logic
⚠️ **L1: Possible duplicate entity creation on retry?**
`do_send` checks `if args.card_id and card_schema_str is None` to decide whether to create the entity. On retry `card_schema_str` is no longer `None` (assigned on first attempt), so no duplication — but the correctness depends on a `nonlocal` side effect, which is a maintenance risk.

⚠️ **L2: `card_schema_str` may leak state across batch recipients**
`card_schema_str` is set via `nonlocal` on the first recipient and reused for the rest. Fine for the current "same card to everyone" requirement, but will break if a future feature wants "per-recipient cards".

### I — Integrity
❌ **I1: SKILL.md does not match code behavior**
SKILL.md example shows `--card-schema` accepting a full Schema JSON, but the code now expects only the `bizData` dynamic payload. Users following the doc will pass the wrong value.

❌ **I2: Parameter description table is stale**
The `--card-schema` parameter description still uses the old semantics.

⚠️ **I3: Card-entity cache has no expiry**
`card_entity_cache.json` is never invalidated; after a schema update, stale `entityId` will silently render the wrong card.

### C — Containment
⚠️ **C1: `args.ref_id = ""` mutates `args` in place**
Consistent with elsewhere in the codebase, but the side effect reaches the entire call chain.

## Summary
| # | Dim | Issue | Severity |
|---|-----|-------|----------|
| L1 | Logic | nonlocal side effect carries retry correctness | ⚠️ WARN |
| L2 | Logic | nonlocal batch-send state reuse risk | ⚠️ WARN |
| I1 | Integrity | SKILL.md example out of sync with code | ❌ ERR |
| I2 | Integrity | SKILL.md parameter table out of sync | ❌ ERR |
| I3 | Integrity | Cache has no invalidation | ⚠️ WARN |
| C1 | Containment | `args.ref_id = ""` mutates global state | ⚠️ WARN |

**Must fix: I1, I2 (SKILL.md doc alignment)**

---

## Example 2: Skill Check — `copy-my-profile`

Target: `skills/copy-my-profile/` entire directory

### G — Grammar
❌ **G1: frontmatter description mixes quote styles**
description uses both straight and CJK quotes: `"I want to copy to other agents"`

### L — Logic
⚠️ **L1: Trigger phrases too broad**
"copy my profile" in description may collide with other skills' triggers; consider a qualifier.

### I — Integrity
⚠️ **I1: SKILL.md references `resources/` but the directory does not exist**
SKILL.md mentions `references/` but the directory was never created.

### C — Containment
⚠️ **C1: SKILL.md exceeds 500 lines**
Body is too long; some content should be moved to `references/`.

## Summary
| # | Dim | Issue | Severity |
|---|-----|-------|----------|
| G1 | Grammar | frontmatter mixed quotes | ❌ ERR |
| L1 | Logic | trigger may be too broad | ⚠️ WARN |
| I1 | Integrity | references nonexistent dir | ⚠️ WARN |
| C1 | Containment | SKILL.md too long | ⚠️ WARN |

**Must fix: G1**

---

## Example 3: Mixed Target — skill with scripts

Target: full skill directory (SKILL.md + send.py + scripts/)

### G — Grammar
⚠️ **G1: 4 leftover `print()` debug statements in `send.py`**
Located at `send.py:1204`, `1210`, `1245`, `1251`; switch to `logging` or remove.

### L — Logic
✅ No issues

### I — Integrity
❌ **I1: SKILL.md claims "file upload supported" but `send.py` does not handle empty files**
`send.py:892` does not check file size; an empty file causes an API error.

⚠️ **I2: `credentials.json` is in `.gitignore` but SKILL.md does not say how to obtain it**
New users following SKILL.md will hit an auth failure.

### C — Containment
⚠️ **C1: `send.py` writes runtime files under `~/.<app>/` without documenting it**
A user cleaning their home directory may delete the runtime cache and lose data.

## Summary
| # | Dim | Issue | Severity |
|---|-----|-------|----------|
| G1 | Grammar | 4 leftover `print()` | ⚠️ WARN |
| I1 | Integrity | Empty-file upload not handled | ❌ ERR |
| I2 | Integrity | How to obtain credentials not documented | ⚠️ WARN |
| C1 | Containment | Runtime file path not documented | ⚠️ WARN |

**Must fix: I1**

---

## Example 4: UGLIC Skill Check — `glic-check` itself

Target: `skills/glic-check/` entire directory. Mode: UGLIC.

### U — User Experience

⚠️ **U1: Step 4 "Severity Escalation" rules are split across multiple places**
Agents must read both step 4 (general rules) and `dimensions.md` (U-specific rules) to get the complete ERR definition. Risk: if an agent only reads the step 4 table and skips the U-specific block, U-dimension severity judgments will be inconsistent.

⚠️ **U2: Mode detection depends on the agent correctly parsing trigger phrases**
SKILL.md lists trigger phrases, but natural language is flexible ("do a uglic on this", "check this with uglic mode"). If the phrasing is outside the list, the agent may fall back to GLIC silently.

ℹ️ **U3: Closing prompt could be tighter**
Step 6's "fix these?" is concise and effective; suggest stronger wording when U has ERR items: "U-dimension ERR directly blocks the user — fix first."

### G — Grammar
✅ No issues

### L — Logic
✅ No issues

### I — Integrity
✅ No issues

### C — Containment
✅ No issues

## Summary
| # | Dim | Issue | Severity |
|---|-----|-------|----------|
| U1 | User Experience | Severity rules split, agents may miss U-specific block | ⚠️ WARN |
| U2 | User Experience | Trigger list may not cover all natural phrasings | ⚠️ WARN |
| U3 | User Experience | Closing prompt does not differentiate GLIC/UGLIC | ℹ️ INFO |

**No must-fix items.** Watch: U1, U2

---

## Example 5: UGLIC Skill Check — large skill (high finding density)

Target: hypothetical `complex-app-registrar` skill — 6 files / 1048 lines, SKILL.md 646 lines, includes scripts + references + workflow with many anti-patterns.

> Real, mature skills with multiple integration paths often produce **12-20 findings** on UGLIC. This is normal and proportional — do not artificially trim to make the report "look cleaner". The goal is honest signal.

### U — User Experience

❌ **U1: SKILL.md 646 lines exceeds 500-line guideline** (silent agent-execution degradation; per U-Agent "SKILL.md length budget" rule)
⚠️ **U2: Step numbering broken** — body says "see Step 6.1.b" but no such section exists
⚠️ **U3: 25 anti-patterns mixed in priority** — critical security mixed with style preferences
⚠️ **U4: Hardcoded absolute paths to sibling skills** (won't work in non-OpenClaw runtimes)
⚠️ **U5: Workflow Step 2 says "Read ALL files in scope" without progressive-read guidance**

### G — Grammar
⚠️ **G1: frontmatter has `metadata`/`version`/`tags` extras** (per I-skill frontmatter discipline rule)
ℹ️ **G2-G3: Mixed CJK/ASCII colons and quote styles**

### L — Logic
❌ **L1: "FATAL: multiple matches" branch has no recovery flow** (silent failure → ERR)
⚠️ **L2-L3: API failure modes undocumented; critical TZ instruction buried in anti-pattern list**

### I — Integrity
❌ **I1: SKILL.md references "Step 6.1.b" — actual section is "7.1.b"** (per I-skill cross-section reference rule)
⚠️ **I2-I4: CHANGELOG.md orphan; `__skill_meta__.json` committed; system-prompt field reading method unspecified**

### C — Containment
⚠️ **C1-C3: Screenshot DSF=2 no fallback; hardcoded token path; 25 anti-patterns smell of tooling debt that should be encoded in preflight scripts**

## Summary
| # | Dim | Issue | Severity |
|---|-----|-------|----------|
| **U1** | UX | SKILL.md > 500 line budget | ❌ ERR |
| U2-U5 | UX | Step ref broken / 25 anti-patterns / hardcoded paths / no progressive-read | ⚠️ WARN ×4 |
| G1 | Grammar | frontmatter extras | ⚠️ WARN |
| G2-G3 | Grammar | Style consistency | ℹ️ INFO ×2 |
| **L1** | Logic | FATAL no recovery | ❌ ERR |
| L2-L3 | Logic | API failure / TZ buried | ⚠️ WARN ×2 |
| **I1** | Integrity | Broken section reference | ❌ ERR |
| I2-I4 | Integrity | Orphan changelog / artifact / undocumented field | ⚠️ WARN ×3 |
| C1-C3 | Containment | DSF / token path / anti-pattern smell | ⚠️ WARN ×3 |

**18 findings total (3 ERR / 13 WARN / 2 INFO).** This is healthy proportion for a complex skill. The 3 ERRs are blocking (must fix before next release), the WARNs cluster around two themes (path portability, doc/workflow organization) that suggest one refactor sweep can address most of them.

**Must fix:** U1, L1, I1
**Should fix:** U2-U5, G1, L2-L3, I2-I4, C1-C2

> Notice: this is a **healthy** complex-skill report. If your check produces 18+ findings and you can't cluster them into 2-3 themes for a refactor sweep, the skill likely needs to be split or rewritten — flag that upfront to the user rather than listing every issue as independent.

---

## What These Examples Demonstrate

1. **ERR vs WARN judgment**: ERR = real breakage, doc-code drift, or user fundamentally blocked. WARN = future risk, maintainability, minor inconsistency, or user friction.
2. **Citation specificity**: Every finding cites `file:line` or section heading.
3. **Severity escalation**: Multiple related WARNs do not auto-escalate to ERR — only escalate when the same issue appears 3+ times **within the same check** (cross-target recurrence does not auto-escalate).
4. **Dimension coverage**: Not every check produces findings. It's fine for a dimension to have zero issues.
5. **Proportionality scales with target size**: 3-6 findings on a small skill (Examples 2, 4); 12-20 findings on a complex skill (Example 5) is healthy if clustered into themes. Don't force-trim or force-pad to a target number.
6. **U dimension targeting**: U is most valuable for skills and tools. On pure code/config, fewer U findings is normal — don't force findings where there is no user-facing surface.
7. **UGLIC vs GLIC**: U findings focus on the experience of using/consuming the skill, not its internal quality. U and G/L/I/C findings can overlap (e.g., a broken instruction is both an Integrity and a User issue) — cite where it matters most.
