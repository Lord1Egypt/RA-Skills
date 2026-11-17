## Description:

Patsnap MCP (open.patsnap.com). Use this skill for ANY Patsnap MCP request — reading, creating, and updating data. Whenever a task involves Patsnap MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and patent analysts use this skill to search Patsnap patent records and review patent details, legal status, citations, and technology landscapes through a connected Patsnap MCP account. It can also submit design FTO workflows and other listed write actions when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a remote installer that was not inspected.

Mitigation: Install a reviewed, pinned oo CLI separately.

Risk: Startup may install additional persistent agent skills.

Mitigation: Review the CLI's skill installation behavior and set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Actions can access account data, upload data, or change Patsnap state.

Mitigation: Authorize only intended account access and uploads, and retain confirmation for write actions.

## Reference(s):

- [Patsnap MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers)
- [Patsnap MCP quickstart](https://open.patsnap.com/devportal/guides/mcp-quickstart)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON, Guidance]

**Output Format:** [Patsnap MCP results in JSON with explanatory text or analysis as requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs and outputs vary; inspect the live action schema before constructing requests.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
