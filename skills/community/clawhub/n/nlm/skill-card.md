## Description:

NotebookLM CLI for listing notebooks, creating notebooks, adding sources, querying notebooks, generating studio artifacts, downloading outputs, sharing notebooks, setting up MCP integrations, and diagnosing auth/install issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsuper](https://clawhub.ai/user/lsuper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate NotebookLM from the terminal, manage notebook content, generate or download NotebookLM outputs, configure MCP integrations, and troubleshoot authentication or installation issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill can require an unpinned third-party CLI package.

Mitigation: Confirm the notebooklm-mcp-cli package source is trusted before installation.

Risk: Sharing and invite commands may expose notebook sources, notes, or generated outputs outside the user's account.

Mitigation: Review notebook contents, recipient addresses, and sharing state before enabling public links or inviting collaborators.

Risk: MCP setup and skill update commands can persistently change local agent configuration.

Mitigation: Review configuration changes and restart or reconnect the target app after setup changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lsuper/skills/nlm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
