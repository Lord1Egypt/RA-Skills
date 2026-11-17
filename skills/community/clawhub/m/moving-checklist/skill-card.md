## Description:

Generate a personalized moving timeline & checklist based on your home info, timeline, and moving distance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and household planners use this skill to generate a personalized moving handbook with a countdown timeline, categorized checklist, household role assignments, and budget estimates for same-city, inter-city, or international moves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moving profiles can include location and household member details.

Mitigation: Use city/district-level locations and pseudonyms rather than full addresses or real household names.

Risk: Generated Markdown may include untrusted profile text when input comes from another person.

Mitigation: Review generated Markdown before sharing, printing, or converting it to another format.

Risk: Budget estimates are generic ranges and China-focused.

Mitigation: Confirm actual mover, cleaning, deposit, shipping, and special-item costs before making decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/moving-checklist)
- [Task Templates](references/task_templates.json)
- [Budget Tiers](references/budget_tiers.json)
- [Input Schema](schemas/input.schema.json)
- [Output Schema](schemas/output.schema.json)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, guidance]

**Output Format:** [Markdown handbook or JSON containing profile, timeline, categorized tasks, role assignment, budget, and handbook fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local CLI output; interactive mode asks for moving profile details, and profile mode accepts JSON input.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
