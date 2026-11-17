## Description:

Review what is due, capture new tasks, build projects from notes, and organize OmniFocus from natural language in OpenClaw on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doannminh](https://clawhub.ai/user/doannminh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users on macOS use this skill to review due work, triage OmniFocus inboxes, and create or reorganize OmniFocus tasks, projects, folders, tags, and perspectives from natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party OmniFocus MCP server that can read, edit, and delete local task data.

Mitigation: Install it only from a trusted source, consider pinning a known-good package version, and review the MCP server registration before use.

Risk: Automation access to OmniFocus can expose or change sensitive personal or work task data.

Mitigation: Start with read-only queries, confirm bulk edits or removals before applying them, and grant macOS automation permissions only when appropriate.

Risk: The skill depends on macOS, OmniFocus Pro scripting support, Node.js, npm, OpenClaw, and the omnifocus-mcp executable.

Mitigation: Run the bundled setup check and resolve missing prerequisites before relying on the skill.

## Reference(s):

- [OmniFocus-MCP upstream project](https://github.com/themotionmachine/OmniFocus-MCP)
- [omnifocus-mcp npm package](https://www.npmjs.com/package/omnifocus-mcp)
- [OmniFocus scripting documentation](https://support.omnigroup.com/documentation/omnifocus/mac/3.12/en/print/)
- [query_omnifocus reference](references/query_omnifocus.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with occasional JSON and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform local OmniFocus reads and writes through the configured MCP server when the user requests them.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
