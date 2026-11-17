## Description:

Search the FBI's Most Wanted list — fugitives, missing persons, and wanted individuals with photos and case details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, journalists, educators, and developers can use this skill to search the FBI Wanted database and retrieve wanted-person case details for awareness, research, or application workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are handled by the Pipeworx gateway.

Mitigation: Use the skill only where sending FBI Wanted search queries to the Pipeworx gateway is acceptable.

Risk: The MCP configuration downloads and runs an unpinned mcp-remote package at startup.

Mitigation: Use a pinned, reviewed mcp-remote version or run the server in a sandbox with limited filesystem, environment-variable, and network access.

## Reference(s):

- [Pipeworx FBI Wanted Pack Homepage](https://pipeworx.io/packs/fbiwanted)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-fbiwanted)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [Markdown or JSON-style summaries of FBI Wanted search results and person details, with MCP configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned records may include titles, descriptions, charges, reward information, images, status, physical descriptions, and case details.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
