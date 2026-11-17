## Description:

This skill should be used when working on Lean 4 formalization projects to maintain persistent memory of successful proof patterns, failed approaches, project conventions, and user preferences across sessions using MCP memory server integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers working on Lean 4 formalization projects use this skill to preserve project-specific proof patterns, failed approaches, conventions, theorem dependencies, and workflow preferences across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memories may retain repository paths, theorem names, tactics, failed attempts, and user preferences beyond the active session.

Mitigation: Review what is stored, clear stale or sensitive memories regularly, and decide before installation whether persistent proof memories fit the project privacy model.

Risk: The documented MCP configuration launches the memory server with unpinned npx -y package resolution.

Mitigation: Pin the MCP memory server version or install it locally before configuring the skill.

Risk: Stored proof patterns can become stale as a Lean project evolves.

Mitigation: Use confidence scoring and periodic review to update, deprecate, or prune memories that no longer match the current project.

## Reference(s):

- [Memory Patterns and Examples](references/memory-patterns.md)
- [MCP memory server docs](https://modelcontextprotocol.io/docs/getting-started/intro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project-scoped memory schemas, retrieval suggestions, MCP server configuration snippets, and helper CLI commands.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
