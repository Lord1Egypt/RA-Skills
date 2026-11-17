## Description:

Comprehensive agentic skills for NEAR Protocol, including gas optimization and on-chain analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mastrophot](https://clawhub.ai/user/mastrophot)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect NEAR network activity, estimate gas costs, compare costs, and get contract gas optimization guidance through OpenClaw-compatible tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs network lookups against NEAR RPC and NearBlocks, which can disclose public account identifiers used in queries.

Mitigation: Treat NearBlocks calls as third-party lookups of public account identifiers and avoid submitting private or sensitive wallet context.

Risk: The npm dependency chain may require updates or isolation before deployment.

Mitigation: Install only in an environment where npm dependencies can be updated or isolated, and review the dependency chain before using the package with private keys or wallet credentials.

## Reference(s):

- [NEAR Agent Skills on ClawHub](https://clawhub.ai/mastrophot/skills/near-agent-skills)
- [NEAR Mainnet RPC](https://rpc.mainnet.near.org)
- [NearBlocks API](https://api.nearblocks.io)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Text, JSON-like objects, arrays of recommendations, and markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-dependent outputs reflect live NEAR RPC and NearBlocks API responses when those services are available.]

## Skill Version(s):

1.0.0 (source: frontmatter, molthub.json, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
