## Description:

Turn stakeholder feedback into agent work packets. A human drops a visual pin on any live web page; your OpenClaw agent reads it via MCP (selector, screenshot, DOM snippet, thread, acceptance criteria), fixes it, and resolves it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcooley8](https://clawhub.ai/user/jcooley8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect OpenClaw agents to Pincushion feedback pins, claim actionable stakeholder feedback, implement fixes, and resolve pins with commit and branch context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable third-party code through npx.

Mitigation: Review the package before use and prefer a pinned pincushion-mcp version when adding the MCP server.

Risk: Cloud sync and browser widget setup can expose page feedback, screenshots, DOM snippets, and stakeholder comments outside the local project.

Mitigation: Use local-only mode unless cloud sync is required, avoid sensitive production pages, and register only intended staging or deployment URLs.

Risk: The optional license key can be mishandled if written into shared project files or committed to the repository.

Mitigation: Store the license key outside the repository or with restrictive permissions and verify it is excluded from version control.

## Reference(s):

- [Pincushion homepage](https://pincushion.io)
- [Pincushion documentation](https://pincushion.io/docs)
- [Pincushion widget script](https://pincushion.io/widget/pin.js)
- [ClawHub skill page](https://clawhub.ai/jcooley8/skills/pincushion)
- [ClawHub publisher profile](https://clawhub.ai/user/jcooley8)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with shell, JSON, and HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js or npx; optional PINCUSHION_LICENSE_KEY enables cloud sync.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
