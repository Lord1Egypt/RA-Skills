## Description:

OpenCloutlook lets an agent read and manage Microsoft Outlook mail and calendar events through Microsoft Graph using PKCE authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrskerrett](https://clawhub.ai/user/jrskerrett)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect an agent to Microsoft Outlook and Calendar so it can summarize mail, search messages, organize folders, list events, and create calendar entries after authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores persistent Microsoft OAuth tokens on the local machine.

Mitigation: Use only on a trusted machine and protect ~/.openclaw/msgraph-tokens.json with restrictive file permissions.

Risk: The auth helper can print the current access token.

Mitigation: Avoid running the token-printing command unless needed for debugging, and never share token output.

Risk: Mail and calendar commands can mutate user data, including moving messages and creating or deleting events.

Mitigation: Require explicit user review and approval before each mutating action.

Risk: The configured Microsoft Graph scopes include read-write mail and calendar permissions plus User.Read.

Mitigation: Use narrower read-only scopes when mutation is unnecessary and remove unused User.Read if it is not needed.

Risk: The LLM integration example can perform mail or calendar changes from model output.

Mitigation: Add a confirmation gate before executing every model-suggested move, event creation, or deletion.

## Reference(s):

- [Skill Guide](skill.md)
- [Setup Guide](references/SETUP.md)
- [API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/jrskerrett/skills/openclaw-msgraph)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Microsoft Graph authentication and configured delegated scopes.]

## Skill Version(s):

1.0.0 (source: release evidence, CHANGELOG, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
