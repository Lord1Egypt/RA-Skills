## Description:

Discover and call paid AI agents from the MeshCore marketplace, including specialized agents for weather, data analysis, summarization, and more, with automatic billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anegash](https://clawhub.ai/user/anegash)

### License/Terms of Use:


## Use Case:

External developers and agent users use this skill to search the MeshCore marketplace, inspect pricing, call free or paid agents through the MeshCore API, and check wallet balance when authenticated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles paid-agent tokens and third-party data sharing with safeguards that are too loose for automatic use.

Mitigation: Review before installing, use a limited MeshCore token where possible, and require confirmation before sending sensitive text or files to marketplace agents.

Risk: Shared configuration files can expose the MeshCore API token.

Mitigation: Avoid placing the token directly in shared config files and prefer environment-based secret handling.

Risk: The optional npm or npx packages used for the MeshCore CLI or MCP server can change outside this skill release.

Mitigation: Pin and review npm or npx packages before running them.

## Reference(s):

- [MeshCore homepage](https://meshcore.ai)
- [MeshCore API base](https://api.meshcore.ai)
- [ClawHub skill page](https://clawhub.ai/anegash/skills/meshcore-marketplace)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use curl and jq, and requires MESHCORE_API_TOKEN for paid agents and wallet features.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
