# Issue Categorization Rules

Every issue found during scoring must be categorized by severity. This
determines fix priority and iteration behavior.

## Critical — Must Fix Immediately

These block skill loading or cause runtime failures. The iteration loop cannot
complete until all Critical issues are resolved.

| Issue | Why Critical |
|-------|-------------|
| Missing `name` in frontmatter | Claude cannot index or trigger the skill |
| Missing `description` in frontmatter | Claude cannot route to the skill |
| Invalid YAML frontmatter syntax | Parsing fails, skill won't load |
| Referenced files don't exist | Runtime errors when agent follows links |
| Broken file paths in support file map | Same as above, leads to tool failures |
| `tools:` instead of `allowed-tools:` | Tools silently ignored, skill can't function |
| YAML list in `allowed-tools:` | Parse error, skill won't load |

## Major — Must Fix

These significantly degrade skill effectiveness. The iteration loop cannot
complete until all Major issues are resolved (after Critical).

| Issue | Why Major |
|-------|----------|
| Weak/vague trigger description | Agent may not recognize when to use the skill |
| Wrong writing voice (2nd person/passive) | Inconsistent with agent execution model |
| SKILL.md > 500 lines without references/ | Overloads context, reduces comprehension |
| Missing "When to Use" section | Agent can't determine applicability |
| Missing "When NOT to Use" section | False activation on wrong tasks |
| Description doesn't specify when to trigger | Skill may never be selected |
| No Gotchas/Pitfalls section | Agent will repeat known mistakes |
| Support file map uses "Purpose" column | Agent doesn't know when to load files |
| No feedback loops in workflow | Errors propagate undetected |
| Missing `license:` in frontmatter | Spec non-compliance, scanner flag |
| Code ratio > 30% | SKILL.md is bloated with code blocks |
| Inline credential paths in SKILL.md | Security scanner flag (Credential Harvesting) |
| Stale data counts in storage layout | Misleading, goes stale immediately |
| Duplicate sections at end of SKILL.md | Confusing, may contradict earlier content |
## Minor — Evaluate Before Fixing

These are polish items. Evaluate each one individually before implementing.
Only fix if clearly beneficial.

| Issue | Evaluation Question |
|-------|-------------------|
| Subjective style preferences | Is this a genuine improvement or just taste? |
| Optional enhancements | Does value justify the added complexity? |
| "Nice to have" improvements | Cost-benefit positive? |
| Formatting suggestions | Would this actually help the agent? |
| Minor wording improvements | Does it change agent behavior? |

## Minor Issue Evaluation Protocol

Before implementing any minor issue fix, answer these three questions:

1. **Is this a genuine improvement?** Does it add real value or just satisfy a
   preference?
2. **Could this be a false positive?** Is the reviewer misunderstanding context
   or the skill's domain?
3. **Would this actually help the agent use the skill?** Focus on functional
   improvements, not aesthetic ones.

Only implement minor fixes that pass all three questions.

## Severity Escalation

If the same issue type appears across 3+ skills in a batch audit:

1. Record it as a library-wide pattern in `decisions.jsonl`
2. Recommend a Forge-level rule change if the pattern indicates a systemic gap
3. Flag it in the batch audit summary as a "library-wide anti-pattern"

Example: If 5+ skills all have "Purpose" columns instead of "When to read",
recommend adding a Forge build gate that rejects support file maps without
conditional language.