## Description:

Provides review-workflow scaffolding for context, evidence, and output. Use at the start of any detailed review to ensure consistent, comparable findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to establish review context, inventory scope, capture evidence, verify findings, and organize a consistent final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial, with medium confidence because some referenced local paths were unavailable.

Mitigation: Check that referenced local paths are present and review the skill's suggested process before relying on its review output; the scan guidance recommends installing only if this uncertainty is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-imbue-review-core)
- [Skill homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, JSON]

**Output Format:** [Markdown review report structure and structured JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides a consistent report outline and a grounded finding format.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
