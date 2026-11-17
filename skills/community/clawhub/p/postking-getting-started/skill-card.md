## Description:

Router skill for PostKing that confirms the active brand, then hands off to the right specialist skill for posts, blogs, landing pages, SEO, or setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsandtea](https://clawhub.ai/user/bitsandtea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing operators use this skill as the PostKing entry point to select an active brand, verify account health, and route requests to the appropriate specialist workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The router exposes guidance for account, billing, publishing, deletion, domain, and API-key operations beyond simple task routing.

Mitigation: Install only after review, grant only the PostKing permissions needed for the intended workflow, and require explicit user confirmation before purchases, publishing, deletions, domain changes, uploads, social account changes, or key creation.

Risk: The CLI can create API keys and may return a plaintext key once.

Mitigation: Treat returned API keys as secrets, avoid logging or repeating them, and revoke keys that are no longer needed.

Risk: Using an unpinned CLI version can change command behavior after review.

Mitigation: Use a pinned, reviewed postking-cli version for controlled deployments.

## Reference(s):

- [PostKing Skill Release](https://clawhub.ai/bitsandtea/skills/postking-getting-started)
- [PostKing MCP Endpoint](https://mcp.postking.app/mcp)
- [Installing postking-cli](artifact/references/install.md)
- [pking command reference](artifact/references/commands.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline MCP tool calls and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May surface PostKing dashboard URLs returned by tools or CLI commands for user review.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
