## Description:

MoltRock provides agent-facing shell workflows for MROCK token verification, vault-related API calls, portfolio lookup, progress reporting, and promotional text generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sloof13](https://clawhub.ai/user/sloof13)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use this skill to work with MoltRock commands, compare the Base vault-share concept with the pump.fun hype token, verify token addresses, query configured vault APIs, and generate status or promotional messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contribution, portfolio, transfer, balance, share, and governance outputs may be unverifiable and should not be treated as proof of financial activity or rights.

Mitigation: Verify deposits, vault shares, transfers, balances, and governance status independently with trusted chain data and official contract addresses before relying on them.

Risk: The skill can send wallet addresses and contribution amounts to the configured API service.

Mitigation: Use only a trusted HTTPS endpoint and avoid sharing wallet addresses or contribution amounts unless the data-sharing implications are understood.

Risk: The package is flagged as suspicious by the server security evidence because documentation overstates real vault, deposit, and cross-chain behavior.

Mitigation: Review the skill carefully before installing, and treat its outputs as guidance or requests rather than confirmed on-chain facts.

## Reference(s):

- [MoltRock ClawHub skill page](https://clawhub.ai/sloof13/skills/moltrock)
- [MROCK pump.fun token](https://pump.fun/coin/7GWc8fiF7jYkigboNCoHuZPwAhk7zqmht2EWFDCipump)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance, JSON]

**Output Format:** [Plain text with optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands call a configured API endpoint and may print API responses when curl and jq are available.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
