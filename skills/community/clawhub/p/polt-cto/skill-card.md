## Description:

POLT platform CTO - manage projects, create tasks, review submissions, and run the POLT ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playdadev](https://clawhub.ai/user/playdadev)

### License/Terms of Use:


## Use Case:

External developers and platform operators use this skill to operate the POLT ecosystem by creating projects and tasks, reviewing submissions, advancing project stages, participating in discussions, and performing moderation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad authority to change POLT platform state, including project advancement, submission reviews, moderation, and token-related actions.

Mitigation: Require explicit confirmation before state-changing actions and keep an audit trail of administrative decisions.

Risk: The configured POLT API host is an unverified tunnel endpoint and administrative API credentials may be exposed to the wrong service if the host is not trusted.

Mitigation: Verify the API host before sending credentials and use narrowly scoped, revocable API keys.

Risk: The security scan summary reports broad platform-changing authority without clear approval safeguards.

Mitigation: Install only for trusted POLT operators and require confirmation before reviews, bans, project advancement, task deletion, public replies, or token-related actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/playdadev/skills/polt-cto)
- [POLT API base URL](https://polt.fun.ngrok.app)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Configuration]

**Output Format:** [Markdown guidance with HTTP request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted POLT API host and bearer API credentials for administrative actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
