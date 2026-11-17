## Description:

Growth helps an agent diagnose the constrained stage in a growth system, choose compounding loops and channels, size experiments and budgets, and produce growth models, tracking plans, lifecycle maps, referral programs, and related operating guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to analyze growth constraints, define defensible metrics, plan acquisition and retention work, forecast targets, and decide which channels or experiments to run, scale, or stop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update or delete persistent local business notes, including finance, project, and contact records, without a built-in approval step.

Mitigation: Require the agent to preview proposed file writes and deletions and obtain approval before applying changes to real business data.

Risk: Growth analysis may involve sensitive business metrics, budgets, contacts, and campaign information stored in local notes.

Mitigation: Use the configured local Clawic paths intentionally, keep credentials as references such as environment-variable or keychain pointers, and avoid storing raw user-level exports.

## Reference(s):

- [ClawHub Growth skill page](https://clawhub.ai/ivangdavila/skills/growth)
- [Clawic Growth skill homepage](https://clawic.com/skills/growth)
- [Growth skill source](artifact/SKILL.md)
- [Growth memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured prose with formulas, tables, plans, definitions, and local-note updates when durable outputs are produced]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local Clawic growth, finance, project, and contact notes under configured paths; credentials are to be stored only as pointers, not values.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
