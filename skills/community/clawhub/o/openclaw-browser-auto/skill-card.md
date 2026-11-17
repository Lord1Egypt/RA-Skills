## Description:

Configures OpenClaw to connect to remote Chrome/CDP browser endpoints for browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyfee](https://clawhub.ai/user/happyfee)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure OpenClaw for remote Chrome/CDP browser automation, including Docker-hosted headless Chrome and hosted browser endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Chrome/CDP control ports can expose browser automation capabilities if reachable from untrusted networks.

Mitigation: Bind CDP to 127.0.0.1 only and do not expose port 9222 to untrusted networks.

Risk: Remote browser sessions may expose sensitive account data or credentials.

Mitigation: Avoid logging into sensitive accounts through remote browser endpoints.

Risk: Container and hosted browser endpoints can introduce supply-chain or credential-handling risk.

Mitigation: Prefer a pinned and verified container digest and keep browserless or provider tokens out of shared configuration where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happyfee/skills/openclaw-browser-auto)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON5 examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup steps, configuration keys, verification commands, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
