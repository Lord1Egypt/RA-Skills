## Description:

Use when designing, writing, building, diagnosing, or revising NodeCoda Source through the authenticated NodeCoda MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nodecoda](https://clawhub.ai/user/nodecoda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design NodeCoda Source, build it into Dify workflow artifacts, and interpret build diagnostics. It supports project lifecycle handling, credential hygiene, and fallback guidance when MCP tooling is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes running a mutable, unpinned npm package with local filesystem, environment, credential, and MCP-startup access.

Mitigation: Use an exact pinned package version or reviewed local install, and limit credentials to narrowly scoped workflow-build access.

Risk: The skill can send workflow source to remote NodeCoda build services.

Mitigation: Review source before build submission and remove secrets, account passwords, and proprietary data that should not leave the local environment.

Risk: Security evidence marks the release as suspicious because future sessions may reuse installed MCP configuration and credential access.

Mitigation: Review installed MCP configuration before deployment and remove or disable unused NodeCoda server entries after evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nodecoda/skills/nodecoda-workflow)
- [Server-resolved GitHub import](https://github.com/nodecoda/nodecoda-skill/tree/main/skills/nodecoda-workflow)
- [NodeCoda skill repository](https://github.com/nodecoda/nodecoda-skill)
- [References index](references/README.md)
- [NodeCoda workflow language reference](references/language-reference.md)
- [NodeCoda MCP contract](references/mcp-contract.md)
- [Public service workflow](references/public-service.md)
- [Dify target capabilities](references/target-capabilities.md)
- [Diagnostics guide](references/diagnostics.md)
- [Failure modes](references/failure-modes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell commands; generated workflow artifacts are YAML files when builds succeed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .ncoda source files, .dify.yaml workflow artifacts, and .build.json build records during use.]

## Skill Version(s):

0.1.0 (source: evidence release and target metadata; artifact frontmatter lists 0.2.35)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
