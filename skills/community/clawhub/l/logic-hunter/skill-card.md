## Description:

Hard-core logic verification and evidence tracing tool based on the "Golden Triangle" knowledge mining framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken0122](https://clawhub.ai/user/ken0122)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and analysts use Logic Hunter to verify claims, weigh source credibility, and surface logical weaknesses in evidence chains before making decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and claims may be sent to external search providers during evidence gathering.

Mitigation: Avoid confidential, personal, or proprietary topics unless the environment's search tooling is approved for that data.

Risk: Evidence scoring can overstate confidence when source classification or logical entropy factors are incomplete.

Mitigation: Review the cited sources, source grades, and red-team critique before relying on the conclusion.

## Reference(s):

- [Logic Hunter ClawHub Release](https://clawhub.ai/ken0122/skills/logic-hunter)
- [OpenClaw Documentation](https://docs.openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown evidence report with confidence scoring, source weights, red-team critique, and risk notice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a Python confidence calculation helper and external search tools when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
