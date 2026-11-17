## Description:

Analyzes smart contracts, token mechanics, permissions, fee flows, upgradeability, market risks, and likely attack surfaces for onchain projects such as ERC-20s, launchpads, vaults, staking systems, LP fee routing, ownership controls, proxy setups, and suspicious token behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrowan](https://clawhub.ai/user/0xrowan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, auditors, and security reviewers use this skill to structure practical reviews of onchain contracts, tokens, launch modules, vaults, staking systems, routers, proxies, and related protocol components. It helps them identify controls, value flows, privileged actions, upgrade risks, token behavior, and open questions before relying on a project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live onchain checks may reveal contracts or investigation targets to public explorers or chain providers.

Mitigation: Use approved providers and avoid submitting confidential, embargoed, or personally sensitive investigation targets unless policy allows it.

Risk: Analysis can be incomplete when source code, ABI, deployment data, or current chain state is missing.

Mitigation: Confirm conclusions against verified source, deployment information, and current chain or explorer data before relying on the findings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xrowan/skills/onchain-contract-token-a)
- [Publisher Profile](https://clawhub.ai/user/0xrowan)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with summary, findings, trust model, token and fee flow, and open questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity-ordered findings, contract or function references, conditionality notes, and requests for missing source, ABI, deployment, or live chain data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
