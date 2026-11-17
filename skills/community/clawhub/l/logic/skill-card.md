## Description:

Logic helps agents start from what must be true before answering instead of responding on autopilot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to make an agent structure ambiguous, strategic, diagnostic, or decision-heavy requests before recommending action. It is intended to surface objectives, constraints, load-bearing variables, mechanisms, and fragile assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create and maintain persistent reasoning notes under ~/logic/ that influence future sessions.

Mitigation: Review, prune, or remove ~/logic/ when persistence is not desired, and inspect that directory before relying on long-lived reasoning state.

Risk: The skill can shape a wide range of strategic, diagnostic, and decision-making answers through its structural reasoning framework.

Mitigation: Treat outputs as reasoning structure rather than final authority, and validate objectives, constraints, assumptions, and recommendations before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/projectsnowwork/skills/logic)
- [Logic Homepage](https://clawic.com/skills/logic)
- [Logic Philosophy](references/philosophy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with occasional shell commands and local state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and maintain local reasoning notes under ~/logic/.]

## Skill Version(s):

1.0.2 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
