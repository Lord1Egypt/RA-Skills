## Description:

Set up or log in to Karma by obtaining, saving, and verifying a KARMA_API_KEY for Karma agent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maheshmurthy](https://clawhub.ai/user/maheshmurthy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill for first-time Karma setup, including quick-start key generation, email login, environment variable configuration, and verification before running Karma action skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if echoed into chat, displayed in full, or written permanently to shell startup files.

Mitigation: Ask before persisting credentials, prefer session-only environment variables when appropriate, and redact API keys in user-facing output.

Risk: Verification commands could send credentials to an unintended endpoint if KARMA_API_URL is overridden.

Mitigation: Use the production Karma HTTPS endpoint by default and only allow trusted local development URLs when the user intentionally opts in.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maheshmurthy/skills/karma-setup-agent)
- [Karma Agent API base URL](https://gapapi.karmahq.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user prompts for setup method, email address, verification code, API key handling, and permission to persist credentials.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
