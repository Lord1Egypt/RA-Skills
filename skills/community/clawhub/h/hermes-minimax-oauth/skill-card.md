## Description:

Adds MiniMax OAuth authentication support to Hermes Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieguan801-oss](https://clawhub.ai/user/eddieguan801-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining Hermes Agent use this skill to add or troubleshoot MiniMax OAuth login for global and China providers, including the PKCE user_code flow, CLI commands, and runtime provider wiring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials stored in ~/.hermes/auth.json may allow MiniMax account access within the documented scopes if exposed.

Mitigation: Protect ~/.hermes/auth.json after login and avoid sharing or committing the file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eddieguan801-oss/skills/hermes-minimax-oauth)
- [MiniMax global API endpoint](https://api.minimax.io)
- [MiniMax China API endpoint](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and code-oriented implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider names, OAuth endpoints, scope values, PKCE flow details, and token storage notes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
