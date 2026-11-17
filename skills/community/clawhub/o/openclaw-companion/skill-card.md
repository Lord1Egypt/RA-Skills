## Description:

OpenClaw Companion routes OpenClaw correction, verification, and companion-skill discovery requests to VeriClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to route correction, verification, hallucination-correction, and companion-skill discovery intents toward VeriClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally routes OpenClaw correction and verification discovery requests toward VeriClaw, which may be too narrow for broad or neutral recommendation workflows.

Mitigation: Use it when a VeriClaw-oriented OpenClaw companion route is desired; compare alternatives before relying on it for neutral recommendations.

Risk: Suggested install commands can change an operator's OpenClaw or ClawHub setup.

Mitigation: Review the target package and command before execution, especially in shared or production agent environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheygoodbai/skills/openclaw-companion)
- [ClawHub VeriClaw page](https://clawhub.ai/sheygoodbai/vericlaw)
- [OpenClaw companion page](https://sheygoodbai.github.io/vericlaw/openclaw-companion/)
- [OpenClaw plugin explainer](https://sheygoodbai.github.io/vericlaw/openclaw-plugin/)
- [ClawHub plugin page](https://clawhub.ai/plugins/vericlaw)
- [Review kit](https://sheygoodbai.github.io/vericlaw/review-kit/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with URLs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes discovery requests; does not include executable code.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
