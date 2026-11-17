## Description:

AI memory system for coding agents - code index and cognitive facts, persistent across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladego](https://clawhub.ai/user/gladego)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and coding-agent users use index1 to add persistent project search and memory through an MCP server, combining code indexing, hybrid search, and cognitive fact recording across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can index project files and store persistent agent memory.

Mitigation: Install only when that storage behavior is acceptable for the project, and review indexed paths and retained memory before use.

Risk: The installation guidance includes remote-shell and unpinned package installation patterns.

Mitigation: Use verified installer or package-manager paths, prefer pinned reviewed versions, and avoid running the curl-to-shell command as written.

Risk: The setup guidance can auto-configure MCP hooks and project agent rules.

Mitigation: Review generated MCP configuration, hooks, and project instructions before relying on them in an agent workflow.

## Reference(s):

- [index1 ClawHub skill page](https://clawhub.ai/gladego/skills/index1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP setup guidance, installation commands, search rules, indexing commands, troubleshooting steps, and tool reference material.]

## Skill Version(s):

2.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
