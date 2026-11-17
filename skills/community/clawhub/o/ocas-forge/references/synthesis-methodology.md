# Synthesis Methodology — Building Skills from Multiple Sources

When creating a new skill that synthesizes knowledge from multiple source skills
and external references, use this workflow:

## Process

1. **Gather sources** — Identify 3-8 related skills (both OCAS and external).
   Read each fully via `skill_view`. For external skills, use `browser_navigate`,
   `browser_snapshot`, and `browser_console` to extract content.

2. **Extract best attributes** — For each source, identify:
   - What it does well (structure, rubric design, severity categorization)
   - What makes it unique (specific sections, workflows, patterns)
   - What to avoid (bloat, vagueness, over-constraint)

3. **Synthesize, don't copy** — Merge the best attributes into a coherent whole.
   The new skill should NOT read as a Frankenstein of its parents. Resolve
   conflicting terminology. Refactor merged content into the parent's existing
   section structure — never use `## Integrated: Name` wrapper sections.

4. **Cross-check against Forge standards** — After writing, run `forge.validate`
   to check: frontmatter completeness, support file map, progressive disclosure,
   code ratio.

5. **Self-assess with skilllab's Critique** — Run the Critique procedure on the new
   skill until it reaches the target score (50/50 for OCAS-authored skills).
   skilllab's Critique section (merged from ocas-critique) contains the full
   6-phase rubric pipeline.

## Anti-patterns

- **Frankenstein synthesis** — Copy-pasting sections from multiple sources
  without refactoring. The result contradicts itself and duplicates guidance.
- **Scope creep** — Trying to include everything from every source. Be
  selective. The new skill needs ONE sharp promise.
- **Missing includes:** — Forgetting `includes: [references/**]` when the skill
  has a references/ directory. This is a Major D1 issue.

## Real-world example

`ocas-critique` was built by synthesizing:
- `review-skill` (10-dimension rubric, scoring bands, common fixes)
- `skill-architect` (Quick Wins, description formula, anti-patterns)
- `skill-improver` (severity categorization, iteration loops)
- `improve-skill` (session extraction mode)
- `ocas-forge` (authoring rules, package patterns)

The synthesis took 2 iterations to reach 50/50 on self-assessment.