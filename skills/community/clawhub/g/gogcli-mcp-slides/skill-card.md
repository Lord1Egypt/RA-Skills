## Description:

Helps agents create, edit, read, and export Google Slides presentations, including speaker notes, slide images, markdown-to-slides flows, template placeholder replacement, and PDF/PPTX export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate Google Slides through gogcli for creating decks, updating slides and notes, copying presentations, and exporting PDF/PPTX files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP package is installed through an unpinned npx command.

Mitigation: Install only when the npm package and publisher are trusted, and consider pinning or otherwise controlling the package version in managed deployments.

Risk: `gog_slides_run` provides a loosely scoped fallback with Google account access.

Mitigation: Review any proposed use of `gog_slides_run` before execution and restrict access to the least-privilege Google account practical.

Risk: The skill can delete, replace, or otherwise modify Google Slides presentations.

Mitigation: Prefer working on copied presentations and review destructive slide operations before allowing an agent to run them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/gogcli-mcp-slides)
- [gogcli](https://github.com/openclaw/gogcli)
- [gogcli MCP repository](https://github.com/chrischall/gogcli-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown responses with JSON MCP configuration examples and file outputs from Slides export tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, modify, copy, delete, replace, or export Google Slides presentations through an authenticated gogcli MCP server.]

## Skill Version(s):

2.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
