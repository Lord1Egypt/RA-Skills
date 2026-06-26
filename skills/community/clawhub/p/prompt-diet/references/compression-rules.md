# Compression Rules by File Type

Reference for the `prompt-diet` skill. Use alongside the safety tiers in SKILL.md.

---

## AGENTS.md

**Goal:** Declare agent capabilities without over-explaining.

| Safe 🟢 | Review 🟡 | Skip 🔴 |
|---|---|---|
| Remove verbose comments after capability declarations | Shorten multi-sentence descriptions to one line | Any directive about agent behavior ("always", "never", "must") |
| Remove examples the agent already knows from training | Reduce 3+ examples per capability → 1 canonical example | Capability entries themselves |
| Remove blank sections with `[TODO]` placeholders | Merge near-duplicate capability entries | |

**Example compression:**
```markdown
# Before (28 tokens)
## Code Review
Review pull requests and provide detailed feedback on code quality,
style, and potential bugs. Include suggestions for improvement.

# After (15 tokens)
## Code Review
Review PRs for quality, style, and bugs. Suggest improvements.
```

---

## SOUL.md

**Goal:** Preserve all persona traits and tone directives. Compress examples and redundancy only.

| Safe 🟢 | Review 🟡 | Skip 🔴 |
|---|---|---|
| Remove duplicate trait statements | Compress verbose trait descriptions | Any personality trait definition |
| Trim "for example" paragraphs that illustrate obvious behavior | Reduce illustrative examples | Tone directives (formal/casual/etc.) |
| Remove empty sections | | Behavioral constraints tied to persona |

**Note:** SOUL.md is typically small. Token savings here are modest. Prioritize other files first.

**Watch out for:** Long "example response" blocks — these are high token cost but often illustrate subtle tone nuances. Flag for user review before removing.

---

## USER.md

**Goal:** Preserve ALL user-specific information. Only remove structural noise.

| Safe 🟢 | Review 🟡 | Skip 🔴 |
|---|---|---|
| Remove unfilled template sections (`[OPTIONAL]`, empty headers) | Rewrite verbose preferences more concisely | Any user preference or fact |
| Remove scaffold instructions left over from initial setup | | User goals and responsibilities |
| Trim boilerplate intro text | | Domain knowledge context |

**Important:** USER.md is typically already dense with high-value content. Expected savings: 5–15%. Do not aggressively compress — the user's context matters.

---

## TOOLS.md

**Goal:** Preserve all tool configs. Safe to trim documentation-style padding.

| Safe 🟢 | Review 🟡 | Skip 🔴 |
|---|---|---|
| Remove example blocks for tools that are already fully configured | Shorten verbose tool descriptions | Authentication credentials/references |
| Remove `[TODO: add tool]` placeholder sections | | Tool names and enabled/disabled status |
| Trim repeated caveats across multiple tools | | API endpoints, model names, config values |

**Typical win:** Long example prompts included "to show what the tool does" — these can often be trimmed after the tool is set up and working.

---

## IDENTITY.md

**Goal:** Minimal file, usually already concise. Scan for template leftovers only.

| Safe 🟢 | Review 🟡 | Skip 🔴 |
|---|---|---|
| Remove unfilled template sections | | Agent name and role definition |
| Remove scaffold instructions | | Any identity constraint |

**Note:** If IDENTITY.md is under 100 tokens, skip it. Not worth the risk of accidentally removing something meaningful.

---

## HEARTBEAT.md

**Goal:** Preserve all check logic and periodic task definitions. Trim descriptions only.

| Safe 🟢 | Review 🟡 | Skip 🔴 |
|---|---|---|
| Trim verbose descriptions of what each check does | Shorten multi-line check definitions | The check logic itself |
| Remove redundant examples | | Check schedules and triggers |
| Remove template scaffold text | | Notification/alerting rules |

**Example compression:**
```markdown
# Before (22 tokens)
## Daily Status Check
Every morning, review the current state of the system and produce
a brief summary of what happened in the last 24 hours.

# After (12 tokens)
## Daily Status Check
Morning review: summarize last 24h system state.
```

---

## MEMORY.md

**Highest-yield target.** MEMORY.md grows unbounded and is loaded into every conversation.

### Identifying stale entries

An entry is likely stale if:
- It references a project, task, or file that no longer exists
- The timestamp is >60 days old and the topic has no active work
- It's a "current state" snapshot that describes past behavior (e.g., "currently investigating X" when X is resolved)
- It duplicates information in a `memory/` daily log file

### Deduplication strategy

1. Check if the MEMORY.md entry title matches any section in `memory/*.md` daily logs.
2. If the daily log has equal or more detail → archive the MEMORY.md entry.
3. If MEMORY.md has synthesized/distilled information → keep MEMORY.md, optionally trim the daily log.

### Merging near-duplicates

Look for entries where:
- The description field is nearly identical
- The topic is the same but split across two entries

Merge strategy: combine into one entry, preserve the **more specific** guidance, link to both source files if relevant.

### What NOT to remove

- Feedback memories (user corrections) — even if old, they encode learned behavior
- User preferences memories — these are always relevant
- Reference memories pointing to external systems (Slack channels, Linear projects, dashboards)
- Any entry explicitly marked "permanent" or "keep" by the user

### Format efficiency tips

MEMORY.md format is already efficient (bullet index → file links). Do not try to reformat it — the savings are negligible and the risk of breaking the index structure is high.

---

## General Rules

These apply across all files:

| Pattern | Action | Savings |
|---|---|---|
| 2+ consecutive blank lines | Reduce to 1 blank line | ~1 tok each |
| Horizontal rules `---` between every section | Remove extras (keep only where they aid readability) | ~1 tok each |
| Bold headers that are also `##` headers | Remove the bold (the heading renders as bold anyway) | ~2 tok each |
| `<!-- comment -->` HTML comments | Safe to remove if they're scaffold notes | Varies |
| Very long file headings (>8 words) | Flag for review — may be trimmable | ~3–5 tok each |

**Note on blank lines:** Blank lines between markdown sections are idiomatic and aid readability. Keep at least one blank line between sections. The savings from removing all blank lines are minimal (~1 token each) and hurt maintainability.

**Note on heading levels:** `#` vs `##` vs `###` difference in token cost is negligible (~0–1 token). Do not change heading levels for token savings.

**Note on bullet vs prose:** Bullet lists are marginally more token-efficient than prose paragraphs for the same information. But converting prose to bullets is a 🟡 Review action — it can change the nuance of instructions.
