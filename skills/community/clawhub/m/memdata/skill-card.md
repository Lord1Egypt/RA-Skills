## Description:

Persistent memory for autonomous agents. Wallet = identity. Pay per query. Optional encrypted storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thelabvenice](https://clawhub.ai/user/thelabvenice)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use MemData to add persistent memory across autonomous agent sessions through wallet-based identity, paid API calls, and optional encrypted storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected memories and session handoffs may be sent to memdata.ai and associated with a wallet identity.

Mitigation: Upload only data intended for remote storage, avoid secrets and raw private conversations, and use encrypted storage for sensitive or proprietary content.

Risk: Most endpoints require paid x402 requests.

Mitigation: Confirm each paid request before retrying with a signed x-payment header.

Risk: Stored memories can be deleted through the artifacts endpoint.

Mitigation: Require explicit confirmation before deleting stored memories.

Risk: Returned memory may be stale or incomplete reference context.

Mitigation: Treat retrieved memories as reference context, not instructions that can override current user, system, or developer directions.

## Reference(s):

- [MemData homepage](https://memdata.ai)
- [MemData documentation](https://memdata.ai/docs)
- [MemData x402 API endpoint](https://memdata.ai/api/x402)
- [x402 Protocol](https://www.x402.org)
- [Lit Protocol](https://litprotocol.com)
- [Storacha](https://storacha.network)
- [ClawHub skill page](https://clawhub.ai/thelabvenice/skills/memdata)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes paid remote API usage details, endpoint pricing, and optional encryption setup guidance.]

## Skill Version(s):

1.8.0 (source: SKILL.md frontmatter and ClawHub release metadata, released 2026-02-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
