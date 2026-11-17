## Description:

OpenClaw DLP Guard is intended to detect prompt injection, sensitive data leaks, and social engineering before automated OpenClaw tasks submit content to external platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danlct27](https://clawhub.ai/user/danlct27)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and automation builders use this skill to add a pre-submission review step for social posts, web forms, external API calls, and shared file outputs. It is meant to pause suspicious automated submissions, notify the owner, and support approve, reject, or review decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence marks the release suspicious because the documented detection rules may be unreliable for prompt-injection protection.

Mitigation: Review the rules before installation and rely on the skill only after the regex patterns are corrected, tested, and matched to the intended threat model.

Risk: Server security guidance says the supported platform scope should be made consistent before relying on the skill.

Mitigation: Confirm which platforms are enabled in configuration and documentation, then disable or remove unsupported targets before deployment.

Risk: The artifact uses owner approval and rejection flows for suspicious submissions, so incorrect classification can block legitimate automation or allow risky content through.

Mitigation: Keep human review enabled for critical and high findings, preserve safe-default rejection on timeout, and monitor decision logs during rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danlct27/skills/openclaw-dlp-guard)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes detection categories, severity guidance, owner notification flow, and safe-default rejection behavior.]

## Skill Version(s):

2.0.0 (source: server release metadata and plugin metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
