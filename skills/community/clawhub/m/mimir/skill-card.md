## Description:

Self-hosted persistent memory for OpenClaw agents via Mimir MCP with hybrid search, memory lifecycle tools, and optional encrypted local storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tcconnally](https://clawhub.ai/user/tcconnally)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure an OpenClaw agent with a self-hosted Mimir MCP server for durable memory, recall, semantic search, journaling, state, and knowledge-graph workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing downloaded binaries and packages that are not verified by the release evidence.

Mitigation: Review the upstream project, verify the exact binary or package, or build from a pinned trusted release before installing.

Risk: The memory database and environment file can contain sensitive agent memories or encryption material.

Mitigation: Use restrictive permissions for ~/.openclaw/.env and the database, and configure an encryption key before storing sensitive memories.

Risk: Exported memories may lose local-only protections if placed in shared, cloud-synced, or git-backed locations.

Mitigation: Avoid exporting memories to shared/cloud/git locations unless they are separately protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tcconnally/skills/mimir)
- [Mimir project website](https://perseus.observer/mimir)
- [Mimir GitHub repository](https://github.com/Perseus-Computing-LLC/mimir)
- [Mimir Python client](https://pypi.org/project/mimir-client/)
- [Mimir Smithery server listing](https://smithery.ai/server/mimir)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup, privacy, operational, and MCP tool-use guidance for agent memory workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
