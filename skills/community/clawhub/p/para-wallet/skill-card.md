## Description:

Create blockchain wallets and sign transactions using Para's MPC infrastructure where the private key never exists in a single place.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adeets-22](https://clawhub.ai/user/adeets-22)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to guide agents through Para REST API workflows for creating MPC wallets, checking wallet readiness, and signing EVM or Solana payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent using this skill can request wallet creation and signatures through the user's Para account.

Mitigation: Require explicit human approval before creating wallets or signing payloads, and review the chain, wallet, payload, destination, amount, and contract or program action.

Risk: Exposure or overbroad use of PARA_API_KEY can allow unauthorized Para API activity.

Mitigation: Protect and scope the API key, store it only in the runtime environment, and rotate or revoke it if exposure is suspected.

Risk: Global npm installation adds supply-chain exposure for users who only need the skill text.

Mitigation: Prefer direct-copy installation of SKILL.md when possible.

## Reference(s):

- [Para Developer Portal](https://developer.getpara.com)
- [Para](https://getpara.com)
- [ClawHub Skill Page](https://clawhub.ai/adeets-22/skills/para-wallet)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PARA_API_KEY and human review before signing blockchain payloads.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
