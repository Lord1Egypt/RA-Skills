## Description:

Navigator helps people learning technical workflows validate what they just did, identify and close one immediate knowledge gap, and checkpoint their work before continuing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT

## Use Case:

External users, learners, and developers use this skill when they need an agent to read a recent command, output, error, code change, or technical step; say whether it worked; explain the single most important gap; help close that gap; and ask for a backup before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may over-prefer a single confident answer for users who need nuance.

Mitigation: Use higher-priority system or developer instructions to require uncertainty, alternatives, or escalation when the situation is ambiguous or high risk.

Risk: The skill is intentionally procedural and may slow broader troubleshooting.

Mitigation: Use it when step-by-step validation, gap closing, and backup checkpoints are desired; switch posture for exploratory work.

## Reference(s):

- [NAVIGATOR ClawHub Skill Page](https://clawhub.ai/contrario/skills/navigator)
- [Publisher Homepage](https://clawhub.ai/contrario)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Markdown or plain text conversational guidance with occasional copy-paste-ready commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sequential interaction loop: validate the prior step, close one gap, then request a backup checkpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
