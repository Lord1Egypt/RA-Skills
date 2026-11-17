## Description:

PayLock Escrow helps agents create and manage non-custodial SOL escrow contracts, verify delivery, release payments, post or bid on jobs, and check trust scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgnvsk](https://clawhub.ai/user/kgnvsk)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to prepare PayLock API calls for SOL escrow contracts, marketplace jobs, agent profiles, delivery verification, fund release, and trust-score checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent toward cryptocurrency contract creation and fund-release actions.

Mitigation: Require manual approval for every transaction and independently verify recipient, payee, amount, and contract ID before submitting PayLock API calls.

Risk: The security summary flags weakly scoped authority and under-disclosed financial risk.

Mitigation: Limit agent autonomy for payment workflows, document financial fees and responsibilities, and route disputed or high-value actions to a human operator.

Risk: Dashboard links based only on agent_id can expose earnings or contract data.

Mitigation: Avoid sharing dashboard URLs or agent IDs outside intended operators, and open dashboard links only in trusted contexts.

## Reference(s):

- [PayLock API Reference](references/api.md)
- [PayLock Full Docs](https://paylock.xyz/paylock.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PayLock endpoint paths, request payloads, contract IDs, agent IDs, wallet addresses, and transaction-review steps.]

## Skill Version(s):

1.0.0 (source: release evidence, created 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
