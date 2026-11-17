## Description:

OpenClaw skill wrapper for installing and operating Lore (NotebookLM automation toolkit) via CLI + MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prantikmedhi](https://clawhub.ai/user/prantikmedhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install Lore locally, complete NotebookLM authentication with user involvement, verify the setup, and configure the Lore MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable third-party code without pinned versions or hashes.

Mitigation: Pin a reviewed Lore commit and notebooklm-skill package version before installation.

Risk: NotebookLM authentication and source materials may expose private session state or user content.

Mitigation: Use an isolated virtual environment and do not print, copy, or commit NotebookLM storage state, cookies, browser profiles, or private materials.

Risk: The MCP process may access unrelated files, browser profiles, environment variables, or private NotebookLM materials.

Mitigation: Limit the MCP process to the minimum required filesystem paths, browser profile, and environment variables.

## Reference(s):

- [Lore project repository](https://github.com/prantikmedhi/lore)
- [ClawHub skill page](https://clawhub.ai/prantikmedhi/skills/notebooklm-lore)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Docs-only wrapper; no executable code is included in the skill artifact.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
