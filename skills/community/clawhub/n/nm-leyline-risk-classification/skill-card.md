## Description:

Classifies agent tasks into 4 risk tiers (GREEN/YELLOW/RED/CRITICAL)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to classify agent tasks by scope and impact, select verification requirements, and assess whether tasks can run in parallel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a confirmed classification gap that could cause risky changes to be underclassified; the scan is partial and notes two unresolved local path references.

Mitigation: Review classification and escalation behavior against your own policy before acting on security-sensitive, data-affecting, or irreversible work, and inspect the unresolved local references before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-leyline-risk-classification)
- [Plugin homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance, Task metadata]

**Output Format:** [Concise risk tier assessment with rationale and verification guidance; may include task metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
