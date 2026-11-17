## Description:

Local-first MCP memory backend and governance console for coding agents. Auto-organize, quarantine, supersede, and rollback shared memories across multiple agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[irisxc4](https://clawhub.ai/user/irisxc4)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use MemoryGuard to provide Claude Code, Codex, and Cursor with a local shared-memory backend that organizes, searches, updates, quarantines, and rolls back agent memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider setup can persistently modify local agent instructions and MCP configuration.

Mitigation: Review proposed changes before installation, run setup manually from a trusted terminal, and back up agent configuration files first.

Risk: Untrusted prompts or repositories could try to invoke provider installation behavior.

Mitigation: Avoid allowing untrusted agent sessions to call memoryguard_provider_install and prefer project-scoped configuration where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/irisxc4/skills/memoryguard)
- [MemoryGuard homepage](https://github.com/irisxc4/memoryguard)
- [PyPI package](https://pypi.org/project/agent-memguard/)
- [Claude Code install guide](docs/install-claude-code.md)
- [Codex install guide](docs/install-codex.md)
- [Cursor install guide](docs/install-cursor.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON MCP tool responses, and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify local agent memory instructions and MCP configuration when provider setup tools are invoked.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
