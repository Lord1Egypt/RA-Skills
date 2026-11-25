## Description:

Wrap an existing Python app or engine as a local stdio MCP server, register it with OpenClaw, and prove the tools actually work. Covers reusing the app venv, the mcp v1 vs v2 rename trap, sys.path for vendored modules, and the "Connection closed" probe failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamant064](https://clawhub.ai/user/adamant064)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers can use this skill to wrap an existing Python application's reusable core as a local stdio MCP server for OpenClaw, without importing its GUI or rewriting its business logic. It guides them through setup and verification of the server and its tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One reference in SKILL.md could not be resolved, leaving scan coverage incomplete.

Mitigation: Review the skill's contents and check the unresolved reference before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/adamant064/skills/mcp-server-from-python-core)
- [Publisher profile: adamant064](https://clawhub.ai/user/adamant064)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup and verification steps; model loading or long-running inference may block a turn.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
