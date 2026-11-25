## Description:

Adds developer-authored annotations to the gauntlet knowledge base

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to capture module-specific insights and rationale that are not apparent from code, then save them as YAML annotations for future gauntlet challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An inaccurate or duplicate annotation could mislead future challenges.

Mitigation: Check the concept and rationale against project context, and check for an existing entry under the same slug before saving.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-gauntlet-curate)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)

## Skill Output:

**Output Type(s):** [Configuration, Guidance]

**Output Format:** [YAML annotation file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Annotation includes a concept and rationale (why); its filename slug is based on the annotated module and concept.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
