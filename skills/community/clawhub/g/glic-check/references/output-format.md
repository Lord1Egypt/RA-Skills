# GLIC / UGLIC Report Format

## GLIC Mode (4 dimensions)

```
## GLIC Check — [brief target description]

### G — Grammar (syntax / format / naming)
[findings, each prefixed with {severity} {tag}]

### L — Logic (control flow / causation)
[findings]

### I — Integrity (completeness / consistency / boundaries)
[findings]

### C — Containment (scope / side effects / security)
[findings]

## Summary
| # | Dim | Issue | Severity |
|---|-----|-------|----------|
| L1 | Logic | [brief description] | ❌ ERR |

**Must fix:** [ERR item tags]
**Should fix:** [WARN item tags]
```

## UGLIC Mode (5 dimensions)

```
## UGLIC Check — [brief target description]

### U — Usability & User Experience
[findings, each prefixed with {severity} tag: U1, U2, ...]

### G — Grammar (syntax / format / naming)
[findings]

### L — Logic (control flow / causation)
[findings]

### I — Integrity (completeness / consistency / boundaries)
[findings]

### C — Containment (scope / side effects / security)
[findings]

## Summary
| # | Dim | Issue | Severity |
|---|-----|-------|----------|
| U1 | Usability & UX | [brief description] | ❌ ERR |
| U3 | Usability & UX | [brief description] | ⚠️ WARN |
| G1 | Grammar | [brief description] | ⚠️ WARN |

**Must fix:** U1
**Should fix:** U3, G1
```

## Finding Format

Each finding follows this pattern:

```
{severity} **{tag}: [one-line description]**
[2-3 sentence explanation with location, impact, and why it matters]
```

Tags: U1, U2, ... (UGLIC only), G1, G2, ... L1, L2, ... I1, I2, ... C1, C2, ...

Numbering resets per dimension and per check. First U finding is always U1, first Grammar finding is always G1.

**U dimension finding format (UGLIC, skill target):**
When checking a skill, U findings may note the perspective in brackets for clarity, but this is optional — use it only when the perspective distinction adds meaningful context:
```
⚠️ U3: [Agent] Step I/O unclear — Step 2 output is not declared as Step 3 input
⚠️ U4: [Human] Prerequisite undeclared — user needs admin rights but the doc never mentions it
```
For code and config targets, U findings are always from the Human perspective unless explicitly tagged `[Agent]`.

## Severity Markers

| Marker | Use When |
|--------|----------|
| `✅` | Dimension has no issues |
| `❌ ERR` | Must fix (functional, security, doc misalignment, **agent cannot execute or user cannot complete core task**) |
| `⚠️ WARN` | Should fix (maintainability, consistency, future risk, **agent uncertainty or user friction/confusion**) |
| `ℹ️ INFO` | Optional (style preference, minor improvement) |

If a dimension has zero issues, **always print the dimension heading first**, then `✅ No issues` on the next line. Do not omit the heading.

```
### U — Usability & User Experience
✅ No issues
```

This keeps the report structure predictable and lets readers verify each dimension was actually evaluated.

## Summary Table

Required at end. Format:

```markdown
## Summary

| # | Dim | Issue | Severity |
|---|-----|-------|----------|
| U2 | Usability & UX | [problem] | ⚠️ WARN |
| G2 | Grammar | [problem] | ⚠️ WARN |
| L1 | Logic | [problem] | ❌ ERR |
| I3 | Integrity | [problem] | ⚠️ WARN |
```

Then list items requiring action:
```markdown
**Must fix:** L1
**Should fix:** U2, G2, I3
```

If no ERR items:
```markdown
**No must-fix items.** Watch: U2, G2, L3
```

## Location Citation

Always cite specific location. Format depends on target:

- Code: `send.py:1860` or `line 221`
- Skill: `SKILL.md line 221` or `SKILL.md "## Usage" section`
- Config: `config.json → channels.hi.accounts`
- Doc: section heading or paragraph number

Bad: "naming inconsistent" / "somewhere in the code"
Good: "`send.py:342` uses `msg_preview`, but the broadcast path at `send.py:2841` does not use it"

## Closing Prompt

After the summary table, always ask:

```
Want me to fix these?
```

For ERR items, fix is expected. For WARN items, offer but don't push. Never auto-fix without confirmation.

## Proportions

A good GLIC/UGLIC report typically has:
- 0-3 ERR items (zero is ideal; more than 5 is a red flag on the change)
- 1-8 WARN items
- 0-3 INFO items

If you find 10+ WARN items, the target likely needs broader refactoring — flag this to the user rather than listing every nitpick.
