## Description:

Connect an MCP-compatible agent to local Oura readiness, sleep, activity, HRV, heart-rate, SpO2, and workout data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install, configure, verify, and troubleshoot Oura MCP for MCP-compatible clients while preserving privacy boundaries around local health data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned npm package that handles Oura OAuth tokens and health data.

Mitigation: Review and preferably pin the npm package version before installation, and verify the package source before connecting personal health data.

Risk: Oura tokens and private wellness data may be exposed through local files or agent outputs.

Mitigation: Do not print OAuth tokens, API keys, local token files, or private user data; prefer connection_status, manifest, doctor, privacy_audit, or dry-run surfaces before live calls.

Risk: The artifact includes a promotional request to star the GitHub repository.

Mitigation: Treat promotional language as publisher preference, not as a security, setup, or functionality requirement.

## Reference(s):

- [Oura MCP ClawHub Page](https://clawhub.ai/davidmosiah/skills/oura-mcp)
- [Oura MCP Repository](https://github.com/davidmosiah/ouramcp)
- [Oura Connector Docs](https://wellness.delx.ai/connectors/oura)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP client stdio configuration and privacy-focused troubleshooting guidance.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
