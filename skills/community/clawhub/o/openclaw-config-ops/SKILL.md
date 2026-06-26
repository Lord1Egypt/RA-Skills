---
name: openclaw-ops
description: Safe OpenClaw gateway configuration operations. Use when reading, analyzing, or modifying openclaw.json. Enforces schema validation + official documentation verification before every change.
---

# OpenClaw Ops

Safe, documented, schema-validated gateway configuration operations.

## When to Use

- **Any** interaction with `openclaw.json`: read, analyze, modify
- `config.get`, `config.schema.lookup`, `config.patch`, `config.apply`
- Adding/removing models, plugins, channels, agents, MCP servers, tools config
- Troubleshooting config validation errors
- Analyzing current config for optimization opportunities

## Two Modes

Determine mode **before** starting any config work.

### Mode A: Analysis Only (no config change)

**Trigger**: user asks to check, review, compare, optimize, or analyze config, **without** providing a specific target value.

Flow:
1. `config.schema.lookup` for relevant keys
2. Official doc verification (see Step 2)
3. Present findings with schema + doc evidence
4. **Stop.** Wait for user instruction.

Output format:
```markdown
## Config Analysis

**Finding**: what was found
**Current state**: relevant config values (from config.get)
**Schema evidence**: what schema.lookup confirmed
**Doc evidence**: source URL or QMD reference
**Recommendation**: suggested change (if any), or "no action needed"
```

**Transitioning to Mode B**: if user responds with explicit approval to execute a recommended change (e.g. "do it", "apply", "yes, modify it"), switch to Mode B. Start from Step 3 (Form Change Proposal) — Steps 1 and 2 evidence from Mode A can be reused.

### Mode B: Modification (config change)

**Trigger**: user explicitly requests a change AND provides sufficient detail (target key + intended value or clear intent). Examples:
- "add model X with id Y"
- "set thinkingDefault to medium"
- "remove the minimax plugin"
- Responding to a Mode A recommendation with "do it" / "apply" / "确认修改"

**Insufficient for Mode B** (fall back to Mode A + ask):
- "帮我改一下配置" without specifying what to change
- "优化一下" without target values
- Vague instructions without concrete config keys or values

Flow: all 6 steps below, in strict order. No step may be skipped.

### Mode Switching Rules

| Situation | Action |
|-----------|--------|
| Mode A analysis done, user says "do it" | → Mode B, start from Step 3 (reuse Steps 1-2) |
| Mode B Step 3 proposal rejected | → Back to Mode A, re-analyze |
| User intent unclear | → Mode A, ask for clarification |
| Emergency config fix needed | → Still Mode B, but note "emergency" in log |

## Mandatory Process — Mode B (6 Steps)

### Step 1: Schema Lookup

```
config.schema.lookup(path="target.config.key")
```

Verify:
- Key **exists** in schema (not invented)
- Type matches intended value
- `enum` values present → only use values from the enum
- `additionalProperties: false` → no extra sub-fields allowed
- Free-form objects (`additionalProperties: {}`) → still verify field names from docs

**Schema has key + config doesn't**: this means the key can be created. Proceed to Step 2.
**Schema lookup fails or key doesn't exist**: STOP. Do not proceed. Report to user.

### Step 2: Official Documentation Verification

**This step is mandatory for both Mode A and Mode B.**

Priority order (use first that works):

| Priority | Method | When to use |
|----------|--------|-------------|
| 1 | `qmd__query` | QMD has OpenClaw docs indexed → fastest, saves tokens |
| 2 | `web_fetch("https://docs.openclaw.ai/<path>")` | QMD unavailable or no results |
| 3 | `exec("openclaw <command> --help")` | Docs site unreachable; **last resort only** |

What to verify:
- Correct parameter names and values
- Required vs optional fields
- Known limitations, version requirements, provider-specific behavior
- Example configurations

**If no documentation source covers the target config**:
- Note explicitly: "No documentation found for <key>"
- Rely on schema alone (type + enum + children)
- Do NOT guess. If schema is ambiguous, ask user.

### Step 3: Form Change Proposal

Present to user:

```markdown
## Config Change Proposal

**Target**: full config key path
**Action**: add / modify / remove
**Current value**: (from config.get, or "does not exist")
**Proposed value**: exact new value
**Schema evidence**: type, enum, constraints from schema.lookup
**Doc evidence**: URL or "QMD:collection/doc-id" confirming correctness
**Impact**: what changes for the user
**Risk**: version constraints, provider limitations, side effects
```

### Step 4: User Confirmation

Wait for explicit user approval. Quote the exact change.

All Mode B operations require confirmation. There are no exceptions — if the user already said "do it", that triggered Mode B, but Step 3 proposal must still be presented and acknowledged.

**When in doubt**: ask. Over-confirming is better than wrong changes.

### Step 5: Backup + Execute

**5a. Backup first** (always, before any modification):

```
exec("cp ~/.openclaw/openclaw.json ~/.openclaw/backups/openclaw-$(date +%Y%m%d%H%M%S).json")
```

If backup fails: STOP. Do not proceed without backup.

**5b. Apply change** (in preference order):

1. `config.patch` — partial updates, **preferred**
2. `config.apply` — only for replacing entire config sections
3. `exec` + Python JSON edit — only when config.patch cannot achieve the change (e.g. removing keys)

**One logical change per operation** — see definition below.

### Step 6: Verify + Log

```
1. config.get(path="target.key") → confirm value applied correctly
2. exec("openclaw config validate") → confirm config is valid
3. If gateway restart triggered → confirm restart succeeded
4. Record change to logs/config-changes.log
```

Change log format (append to `~/.openclaw/workspace/logs/config-changes.log`):
```
## YYYY-MM-DDTHH:MM:SS+08:00
- action: add|modify|remove
- target: config.key.path
- old_value: <previous value or "N/A">
- new_value: <new value>
- reason: <brief justification>
- schema_verified: true
- doc_source: <URL or "QMD:collection/doc-id">
- user_approved: true
- backup: <backup file path>
```

## Definition: "One Logical Change"

A logical change = **changes to keys within the same config subtree that serve a single user intent**.

| Example | Count | Reason |
|---------|-------|--------|
| Add one model entry | 1 | Single intent, one subtree |
| Add model + set it as fallback | 1 | Same intent (add fallback model), same subtree |
| Add model + add plugin + change channel | 3 | Different subtrees, different intents |
| Modify 3 unrelated fields in tools.* | 3 | Different intents, must be separate patches |

**Rule of thumb**: if you need to mention two different top-level config sections in one proposal, split it.

If in doubt, **split**. Smaller patches are safer and easier to roll back.

## Hard Prohibitions

- ❌ **Guess field names or values** — always verify via schema + docs
- ❌ **Skip schema.lookup** — even for "obvious" or "previously used" keys
- ❌ **Skip doc verification** — even when you "already know" the config
- ❌ **Use external blogs/GitHub issues as config source** — clues only, never evidence
- ❌ **Bundle unrelated changes** — one logical change per patch
- ❌ **Modify config without backup** — Step 5a is mandatory
- ❌ **Modify config without logging** — every change must go to config-changes.log
- ❌ **Proceed after schema lookup failure** — STOP and report
- ❌ **Assume prior knowledge replaces verification** — "I've done this before" is not evidence
- ❌ **Skip user confirmation** — all Mode B operations require Step 4

## Documentation Quick Reference

| Topic | URL |
|-------|-----|
| Config reference | `https://docs.openclaw.ai/gateway/configuration-reference` |
| Config examples | `https://docs.openclaw.ai/gateway/configuration-examples` |
| Models | `https://docs.openclaw.ai/models/` |
| Plugins | `https://docs.openclaw.ai/plugins/` |
| Channels | `https://docs.openclaw.ai/channels/` |
| Tools | `https://docs.openclaw.ai/tools/` |
| MCP | `https://docs.openclaw.ai/tools/mcp` |
| CLI reference | `https://docs.openclaw.ai/cli/` |
| Security | `https://docs.openclaw.ai/gateway/security` |
| Sandbox | `https://docs.openclaw.ai/gateway/sandboxing` |
| Skills | `https://docs.openclaw.ai/tools/skills` |
| Multi-agent | `https://docs.openclaw.ai/concepts/multi-agent` |
| CLI backends | `https://docs.openclaw.ai/gateway/cli-backends` |
| Thinking levels | `https://docs.openclaw.ai/tools/thinking` |
| apply_patch | `https://docs.openclaw.ai/tools/apply-patch` |
| Web search | `https://docs.openclaw.ai/tools/web-search` |
| TTS | `https://docs.openclaw.ai/tools/tts` |
| Image gen | `https://docs.openclaw.ai/tools/image-generation` |
| Music gen | `https://docs.openclaw.ai/tools/music-generation` |
| Providers | `https://docs.openclaw.ai/providers/<provider-name>` |

## Schema Drill-Down

For nested structures, lookup sub-paths incrementally:

```
config.schema.lookup(path="agents.defaults.cliBackends")
config.schema.lookup(path="agents.defaults.cliBackends.*")
config.schema.lookup(path="agents.defaults.cliBackends.*.sessionMode")
```

Each level returns type, enum, children, and hints.

## Error Recovery

| Problem | Action |
|---------|--------|
| Gateway won't start | `openclaw config validate --json` → find specific errors |
| Unknown key error | Restore from backup → `openclaw config unset <path>` |
| Type mismatch | Schema lookup for expected type → fix value → re-verify |
| Plugin fails to load | Check plugin docs for required config fields |
| config.patch rejected | Check schema for `additionalProperties: false` → verify all sub-fields |
| Patch succeeds but wrong value | Restore from backup → redo with correct value |

## Scope

This skill covers `openclaw.json` configuration only.

- **Workspace files** (SOUL.md, AGENTS.md, etc.): follow workspace rules
- **Skill creation**: use the skill-creator skill
- **Plugin development**: follow plugin docs
