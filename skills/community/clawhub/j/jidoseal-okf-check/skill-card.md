## Description:

Check a folder of Markdown docs against OKF v0.2 (Bronze, Silver, Gold) with the local jidoseal-mcp scanner, fill the missing frontmatter fields, and rescan. Works in Claude Code, Copilot, Cursor, Codex, Gemini CLI or a local model. Nothing leaves your machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oocm147](https://clawhub.ai/user/oocm147)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation maintainers, and teams with Markdown knowledge bases use this skill to check OKF frontmatter completeness, plan safe field additions, apply user-approved fixes, and rescan for Bronze, Silver, or Gold tier evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external local jidoseal-mcp dependency is not version-pinned.

Mitigation: Review the package before installing and pin or audit the version used in controlled environments.

Risk: The skill can edit Markdown frontmatter in a user-selected folder.

Mitigation: Use version control or a backup, review the proposed changes, and approve writes only after confirming the plan.

Risk: Optional certificate checkout can contact the network.

Mitigation: Start checkout only after the user explicitly confirms that they want to buy the paid certificate.

## Reference(s):

- [JidoSeal](https://jidoseal.com)
- [JidoSeal MCP install and wiring](https://github.com/Jidoseal/jidoseal-mcp#install-and-wire-it-into-your-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with scan summaries, proposed frontmatter changes, and inline shell commands or configuration snippets when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may edit Markdown frontmatter only after user consent and relies on a local jidoseal-mcp scanner.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
