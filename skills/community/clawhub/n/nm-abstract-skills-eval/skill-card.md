## Description:

Evaluate Claude skill quality through auditing

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use the skill to assess skill structure, content quality, activation reliability, token efficiency, and tool integration, then prepare audit findings and prioritized improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags guidance that may involve agent settings or other installed skills, along with potentially ambiguous cleanup advice; some referenced local scripts were not analyzed.

Mitigation: Before installing or following troubleshooting advice, review whether the task needs configuration or cross-skill access, inspect the referenced scripts, and check cleanup steps for effects on unrelated work or data.

## Reference(s):

- [Project homepage listed in Clawdis metadata](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-skills-eval)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Audit findings, scores, and improvement plans in Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings and recommendations are tailored to the supplied skill or skill directory.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
