## Description:

Provides sanitization guidelines for external content in skills and hooks

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use these guidelines when building skills or hooks that process untrusted external content. The checklist helps them reduce instruction injection and unsafe code execution risks while applying handling appropriate to the source's trust level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan coverage is incomplete and two local references could not be resolved, leaving their contents unassessed.

Mitigation: Inspect and scan those references before installing or using the skill.

## Reference(s):

- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown checklist and policy guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human-readable handling guidance for external content; no executable output.]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
