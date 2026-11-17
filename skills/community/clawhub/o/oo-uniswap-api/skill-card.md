## Description:

Uniswap API (uniswap.org). Use this skill for ANY Uniswap API request — reading, creating, and updating data. Whenever a task involves Uniswap API, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the OOMOL-connected Uniswap API to request trade quotes, check token approvals, and prepare swap transaction calldata. Inspect each action's schema first and keep confirmation enabled when creating a swap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs unverified remote code without a user checkpoint.

Mitigation: Review and approve CLI installation separately, preferably from a verified release, before running setup.

Risk: Using the connected service gives OOMOL access to API credentials and submitted trade information.

Mitigation: Use the connection only if OOMOL is trusted with those credentials and trade details; keep confirmation enabled for swap creation.

## Reference(s):

- [Uniswap API documentation](https://api-docs.uniswap.org/)
- [Uniswap](https://uniswap.org)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands, Transaction calldata]

**Output Format:** [JSON API responses and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns quote and approval data or swap transaction calldata; on-chain execution is not described.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
