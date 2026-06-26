---
name: skill-builder
description: >
 Builds lean SKILL.md-based skills: decides when a skill is justified, drafts
 a minimal skill skeleton, and audits existing skills for bloat and drift. Use
 when creating a new skill, tightening an existing one, or deciding whether
 the right answer is a plain edit, an existing tool, or a subagent instead.
 Also use when reviewing a skill's trigger description, restructuring a bloated
 SKILL.md, or moving detail into references. Even if the user just says
 "should this be a skill?" or "this skill feels too big," use this.
---

# Skill Builder

Use this skill when the job is to **decide, build, or audit a skill itself**.

This is a narrow builder, not a meta-agent and not a skill factory. Prefer the
smallest useful answer.

## Modes

1. **Decide** — choose between plain edit, existing tool/skill, subagent, or a lean skill
2. **Build** — draft a minimal skill skeleton only when a skill is justified
3. **Audit** — tighten or lightly restructure an existing skill

## Use when

- deciding whether a new skill is justified at all
- drafting a lean new skill skeleton after deciding a skill is warranted
- tightening an existing skill's trigger description or scope
- moving detail out of `SKILL.md` into `references/`
- auditing a skill for bloat, stale instructions, duplicate content, or spec drift

## Do not use when

- a plain file edit will solve the problem faster
- an existing tool or installed skill already covers the work
- the problem is implementation labor across many files rather than reusable guidance
- you are inventing process theater to justify a skill
- you are trying to generate a large framework of boilerplate, governance, or publishing machinery

## Default workflow

1. **Run the decision tree first**
 Read `references/decision-tree.md` and choose between plain edit, existing
 tool/skill, subagent, or a lean skill.

2. **If the answer is not "use a skill," stop there**
 Prefer the honest recommendation over unnecessary skill creation.

3. **If a skill is justified, build the smallest workable skeleton**
 Read `references/supporting-files-guide.md` and produce only what is earned:
 - skill folder
 - `SKILL.md`
 - `references/` with 1-3 files only if they reduce context load or hold optional detail
 - `assets/` only if the skill produces output that depends on bundled files
 - `scripts/` stub only if deterministic execution is clearly warranted

4. **Write the skill body well**
 Read `references/writing-patterns.md` for guidance on voice, examples,
 output templates, and explaining the why behind instructions.

5. **Keep `SKILL.md` minimal**
 Include only:
 - clear frontmatter (`name`, `description`) — see `references/frontmatter-patterns.md`
 - scope and non-scope
 - default workflow
 - reference pointers when optional detail is useful

6. **Smoke test before shipping**
 Try 2-3 realistic prompts against the skill before calling it done:
 - one clear trigger (should activate the skill)
 - one edge case (should activate but tests a boundary)
 - one near-miss (should *not* activate — tests specificity)

 If any of these behave wrong, revisit the description or workflow before shipping.

7. **Audit before expanding**
 Use `references/audit-checklist.md` to remove bloat, stale claims, weak triggers,
 duplicate guidance, and files that do not earn their keep.

8. **Apply the Tool Addition Gate lightly**
 If the proposed skill is compensating for a missing primitive, check this order:
 existing tools → lean skill → subagent/retrieval pattern → new tool only if clearly needed.

## Build output

When building, produce the smallest useful package in this order:

1. **Recommendation**
 State whether the answer is:
 - **Use a skill**
 - **Use the existing tool/skill**
 - **Use a subagent**
 - **Do nothing special; just edit it**

2. **Folder tree**
 Show a minimal tree such as:

 ```text
 skill-name/
 ├── SKILL.md
 └── references/
 └── optional-file.md
 ```

3. **Draft frontmatter**
 Provide only:
 - `name`
 - `description`

4. **`SKILL.md` outline**
 Include only the sections the skill actually needs.

5. **Optional additions**
 Suggest 1-3 `references/` files if justified.
 Suggest an `assets/` folder only if the skill needs bundled templates or static files.
 Suggest a `scripts/` stub only if exact repeatable execution matters.
 Optionally suggest publish metadata ideas (description/tags), but do not package or publish.

### Minimal build example

```text
Recommendation: Use a skill

skill-name/
├── SKILL.md
└── references/
 └── checklist.md
```

```yaml
name: skill-name
description: Helps with X. Use when the user asks for Y or needs Z.
```

`SKILL.md` should then contain only:
- scope / non-scope
- default workflow
- pointer to `references/checklist.md`

## Good outcomes

- A plain edit stays a plain edit
- An existing skill gets tightened instead of replaced
- A new skill has a sharp trigger description and a short `SKILL.md`
- A new skill skeleton is minimal and immediately editable
- Supporting files exist only when they reduce context load or improve reliability
- The skill triggers correctly on natural phrasings (not just its literal name)

## Avoid

- turning one-off work into a permanent skill
- adding README, changelog, install notes, or setup clutter inside the skill unless publishing truly needs it
- stuffing examples, schemas, and edge cases into `SKILL.md`
- creating scripts for things that are better as instructions
- inventing governance layers, registries, dashboards, or lifecycle systems
- writing ALWAYS/NEVER/CRITICAL in all caps instead of explaining reasoning

## Works well with

This skill handles the **pre-flight** phase: deciding if a skill is warranted and
structuring the smallest viable version. For **testing, iteration, and benchmarking**
of a built skill, hand off to `skill-creator` (if available), which provides eval
runners, comparison viewers, and description optimization loops.

## References

- `references/decision-tree.md` — choose skill vs tool vs subagent vs plain edit
- `references/frontmatter-patterns.md` — lean frontmatter, description patterns, and pushy trigger guidance
- `references/writing-patterns.md` — voice, examples, output templates, and instruction style
- `references/supporting-files-guide.md` — progressive disclosure model and what belongs in each folder
- `references/audit-checklist.md` — fast bloat/spec-drift review

## Output style

Lead with the recommendation, then provide only the smallest justified build or edit plan.
