## Description:

Query official Microsoft documentation for concepts, tutorials, best practices, working code samples, API signatures, and SDK troubleshooting across Microsoft technologies such as Azure, .NET, M365, Windows, Power Platform, Teams, and Dynamics 365.

This skill is ready for commercial/non-commercial use.

## Publisher:

[partychen](https://clawhub.ai/user/partychen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical agents use this skill to search, fetch, and summarize Microsoft Learn documentation and code samples when answering questions or debugging Microsoft-related code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance installs @microsoft/learn-cli without pinning an exact reviewed version.

Mitigation: Pin @microsoft/learn-cli to a reviewed exact version and prefer a local project install or controlled environment before use.

Risk: The skill may make broad Microsoft documentation lookups in response to Microsoft-related questions.

Mitigation: Review returned documentation links and excerpts for relevance before using them in user-facing answers or code changes.

## Reference(s):

- [Microsoft Learn documentation](https://learn.microsoft.com/)
- [ClawHub skill page](https://clawhub.ai/partychen/skills/microsoft-learn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with documentation links, excerpts, code samples, and suggested CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search returns up to 10 results; fetch can limit returned page content with max-chars.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
