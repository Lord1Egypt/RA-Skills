## Description:

Teach an agent to install Movi's local MCP server, stay review-first, and use the safest manifest and batch-analysis tools before deeper mutation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to attach Movi as a local MCP server, inspect jobs and manifests, and keep batch work review-first before any patch or apply action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path asks users to run code from a mutable GitHub checkout.

Mitigation: Pin the Movi repository to a reviewed commit or signed release, verify launcher script hashes, and prefer npm ci with a lockfile before attaching the MCP server.

Risk: Manifest patch and apply tools can mutate review data if used too early.

Mitigation: Start with jobs.list, review_queue.get, manifest.get, and analyze.create; treat patch and apply tools as explicit user-approved actions only.

## Reference(s):

- [Movi Review-First Bundle on ClawHub](https://clawhub.ai/xiaojiou176/skills/movi-review-first-bundle)
- [Install And Attach Movi MCP](references/INSTALL.md)
- [Movi MCP Capabilities](references/CAPABILITIES.md)
- [First-Success Path](references/DEMO.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [OpenHands MCP Configuration](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP Configuration](references/OPENCLAW_MCP_CONFIG.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow emphasizes review-first inspection and requires explicit user approval before mutation tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
