## Description:

Prepare product profiles and directory-tailored variants for launch sites (PeerPush, Uneed, …), inspect listing readiness, and read cached directory SEO metrics via the openquok CLI or hosted MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ratimon](https://clawhub.ai/user/ratimon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to prepare launch-site profiles, check directory listing readiness, and review cached SEO metrics through OpenQuok CLI or hosted MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit OpenQuok profiles and competitor settings and request analytics refreshes; it is not read-only.

Mitigation: Specify the intended workspace, profiles, competitors, and refreshes before execution.

Risk: CLI actions depend on credentials and the separate openquok-core skill for authentication and shell safety.

Mitigation: Review openquok-core before providing credentials; directory submissions remain the user's action.

## Reference(s):

- [OpenQuok directory launch CLI documentation](https://www.openquok.com/docs/cli-usages/directory-launch)
- [OpenQuok MCP tools reference](https://www.openquok.com/docs/mcp-references/tools)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Analysis]

**Output Format:** [Markdown guidance and CLI/MCP JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform remote profile and competitor changes or request analytics refreshes when directed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
