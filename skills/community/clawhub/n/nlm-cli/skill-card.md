## Description:

Nlm Cli helps agents use Jacob Brown's notebooklm-mcp-cli (nlm) to automate NotebookLM notebooks, sources, Studio generation, research, sharing, MCP setup, and artifact downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felixhsp](https://clawhub.ai/user/felixhsp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to install, authenticate, and run nlm commands for NotebookLM workflows, including adding sources, querying notebooks, generating Studio artifacts, and downloading outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party CLI package that can affect NotebookLM workflows.

Mitigation: Install notebooklm-mcp-cli only from a trusted package source, review the package/version before use, and prefer an isolated environment.

Risk: NotebookLM operations depend on the active Google account or profile.

Mitigation: Run login checks and confirm the active profile before reading, modifying, sharing, or deleting notebook content.

Risk: Share, delete, setup, and skill install commands can change notebook visibility, remove content, or modify AI-tool configuration.

Mitigation: Confirm the target notebook, recipients, public/private state, destination tool, and reversibility before executing those commands.

## Reference(s):

- [CLI command reference](references/cli-commands.md)
- [Install and authentication guide](references/install-and-auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a local Node wrapper that forwards commands to the nlm CLI.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
