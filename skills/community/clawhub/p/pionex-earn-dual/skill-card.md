## Description:

Use this skill for Pionex Dual Investment workflows, including listing supported pairs and products, checking yield rates or index prices, querying balances or investment history, and preparing user-confirmed invest, revoke, or collect actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pibrandon](https://clawhub.ai/user/pibrandon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to work with Pionex Dual Investment products through pionex-trade-cli. It supports product discovery, yield and index checks, account and history queries, and user-confirmed invest, revoke, or collect workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned global npm CLI install for Pionex tooling.

Mitigation: Install only from a trusted Pionex npm package source and review the package source before using it with account credentials.

Risk: Private commands can access account information or perform Earn actions when API credentials are configured.

Mitigation: Use a dedicated API key with the minimum required View or Earn permission, never grant withdrawal permission, and confirm every real invest, revoke, or collect action.

Risk: Dual Investment write operations can be incorrect if stale yield values, inferred product IDs, or the wrong order state are used.

Mitigation: Run price and state checks immediately before action, use dry-run output first, and require user confirmation for product IDs, client order IDs, and execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pibrandon/skills/pionex-earn-dual)
- [Pionex homepage](https://www.pionex.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run review and explicit user confirmation are expected before write operations.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
