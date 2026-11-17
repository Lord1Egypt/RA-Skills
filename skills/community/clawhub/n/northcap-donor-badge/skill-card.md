## Description:

Support the Northcap Group agent collective: donate USDC on-chain (Ethereum/Base/BSC), get verified and receive a public Supporter/Builder/Partner badge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to register on-chain USDC donations to Northcap Group, verify the transaction through the Northcap donation API, and receive a public donor badge. The workflow is intended for users who accept that donor registry entries and transaction details are public.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan verdict is suspicious because the visible donation flow is disclosed, but the package also contains mismatched compiled Python code that points to an undisclosed IP address.

Mitigation: Review before installing, remove or explain the packaged compiled Python file, and verify the endpoint and wallet independently before using the donation flow.

Risk: Donation registration sends a transaction hash, agent ID, amount, badge level, date, and optional note to a public donor registry linked to on-chain wallet activity.

Mitigation: Use only a real transaction hash, avoid personal identifiers or secrets in the agent ID or note, and proceed only when public disclosure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/northcap-donor-badge)
- [Northcap donation API](https://api.northcapgroup.com/v1/donate)
- [Northcap public donor registry](https://api.northcapgroup.com/v1/donors)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown instructions with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and network access to https://api.northcapgroup.com; donor registry output is public.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
