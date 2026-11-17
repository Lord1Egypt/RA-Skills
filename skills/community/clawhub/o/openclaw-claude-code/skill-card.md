## Description:

Control Claude Code via MCP protocol to execute commands, manage sessions, search and edit code, and coordinate agent teams for development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enderfga](https://clawhub.ai/user/enderfga)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to delegate coding tasks to Claude Code, run shell and file operations, manage persistent coding sessions, and coordinate specialized agent roles across a project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke Claude Code tools that execute commands and read or write project files.

Mitigation: Use it only in trusted, isolated project directories and prefer plan or default permission modes for review before changes are applied.

Risk: Broad tool access or bypass-style permission modes can reduce operator control over file, command, and agent actions.

Mitigation: Restrict allowed tools to the minimum needed and avoid skip-permissions or bypassPermissions modes.

Risk: Custom backend URLs and MCP server subprocesses can expose work to untrusted services or packages.

Mitigation: Use authenticated local or trusted HTTPS backends, pin MCP server packages, and run third-party MCP servers with a minimal environment.

Risk: Example MCP configuration includes token-shaped placeholders for external services.

Mitigation: Do not store real tokens in MCP JSON configs; supply secrets through an approved secret-management path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enderfga/skills/openclaw-claude-code)
- [Publisher profile](https://clawhub.ai/user/enderfga)
- [README](artifact/README.md)
- [MCP configuration example](artifact/mcp_config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, command-line output, JSON tool responses, source code, configuration snippets, and file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream session responses and may produce persistent project changes through Claude Code tools.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
