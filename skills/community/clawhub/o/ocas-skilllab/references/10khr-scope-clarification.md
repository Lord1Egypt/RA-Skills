# 10khr Scope Clarification

## When to Use 10khr Mode

10khr ("10,000 hour grinding") is a LIBRARY-WIDE convergence loop. It scores ALL skills in a library against the 10-dimension critique rubric, ranks them, fixes the lowest-scoring one, and repeats until all pass the quality bar (≥35/50, band B).

## What 10khr Is NOT

- 10xEng autofix (dead code removal, py_compile, import cleanup)
- A single-file script optimizer
- A tool for fixing one specific bug

## Scope Ambiguity in User Requests

When a user says "run 10khr on X," they might mean:

| Request | Meaning | Tool |
|---------|---------|------|
| "10khr on ocas-skilllab" | Critique the skilllab skill itself against the rubric | skilllab critique procedure |
| "10khr on all ocas- skills" | Score all 32 ocas- skills, fix lowest until convergence | skilllab 10khr mode |
| "10xeng autofix on ocas-skilllab" | WRONG — autofix is for code, not skills. Run autofix on the skill's scripts if they need code cleanup, but that's not "fixing the skill" | 10xeng-autofix (on scripts only) |

## Key Distinction

**Code autofix** (10xeng-autofix): py_compile, dead imports, unused functions, copy-paste duplication. Target: `.py` files.

**Skill 10khr** (skilllab critique): 10-dimension rubric scoring (frontmatter, description, conciseness, structure, clarity, freedom calibration, error handling, progressive disclosure, scripts quality, completeness). Target: SKILL.md + references/ + scripts/ as a documentation package.

## Pitfall: Running Code Autofix on a Skill

If you run 10xeng-autofix on a skill directory:
- It will run py_compile on the skill's scripts (valid but incomplete)
- It will NOT critique the SKILL.md (the actual skill content)
- It will miss the 10 dimensions that matter for skill quality
- It may "fix" script issues that were intentional (interactive prompts for agent use, etc.)

**Correct approach:** Use skilllab critique for skills. Use 10xeng-autofix for code repos. The scripts inside a skill can get autofix as a separate operation, but that's not "10khr on the skill."

## Lesson (2026-06-22)

User said "run 10xeng:autofix on ocas-skilllab." I ran autofix on the 3 scripts inside the skill. Technically valid (they're Python), but completely missed the point — the user wanted the SKILL critiqued, not its scripts compiled-checked. The skilllab's own critique procedure is the right tool.