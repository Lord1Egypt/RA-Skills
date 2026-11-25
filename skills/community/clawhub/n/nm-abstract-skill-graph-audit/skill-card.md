## Description:

Audit Skill() refs; detect hubs, isolates, and dangling targets

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining skill plugins use this skill to map Skill() references, find hubs and orchestrators, identify isolates and dangling targets, and guide documentation or refactoring reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had partial coverage because some local references could not be resolved.

Mitigation: Check the complete plugin and its referenced files before relying on the audit or installing the skill.

Risk: Graph counts can miss references expressed through bare skill names and can overcount common words; a zero count alone does not establish that a skill is unreachable.

Mitigation: Inspect likely routers, commands, and dependencies before treating counts as evidence for retiring or consolidating a skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-abstract-skill-graph-audit)
- [Skill metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Plain-text summary or JSON graph report, with Markdown interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Skill(plugin:name) references; module-level dependencies and self-references are not counted.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
