## Description:

Operate mempool.space public Bitcoin and Lightning explorer APIs through UXC with a curated OpenAPI schema, no-auth setup, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query public mempool.space Bitcoin and Lightning explorer data through UXC, including fee estimates, mempool state, block height, address or transaction status, and Lightning node/channel reads. It is intended for read-only exploration and automation that can tolerate public explorer freshness and privacy constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can use a mutable remote OpenAPI schema that may change after review.

Mitigation: Prefer the bundled local schema or a pinned schema commit with a verified hash before linking the CLI.

Risk: Public explorer queries can disclose addresses, transactions, Lightning public keys, or channel identifiers to the service.

Mitigation: Avoid querying identifiers considered private, and use narrow reads that expose only the data needed for the task.

Risk: Bitcoin mempool data and Lightning rankings change quickly.

Mitigation: Re-query live endpoints before making decisions instead of relying on cached values.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/mempool-space-public.openapi.json)
- [mempool.space public API endpoint](https://mempool.space/api)
- [Official mempool repository](https://github.com/mempool/mempool)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/mempool-space-openapi-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown with inline shell commands and JSON-oriented API output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public API operations; responses may reflect live mempool.space state.]

## Skill Version(s):

1.0.0 (source: server release evidence and OpenAPI schema)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
