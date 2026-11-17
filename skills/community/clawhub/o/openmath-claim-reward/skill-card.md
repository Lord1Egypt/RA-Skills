## Description:

Claims earned rewards from the OpenMath platform by helping users query claimable imported/proof rewards and withdraw verified Shentu rewards after proof verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bennyzhe](https://clawhub.ai/user/bennyzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check claimable OpenMath reward buckets for a Shentu address and prepare confirmed withdrawal commands through a local Shentu keyring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reward queries and withdrawals depend on a trusted local shentud binary and the selected Shentu RPC node.

Mitigation: Install and use only trusted local binaries, and confirm the node URL before querying or broadcasting transactions.

Risk: Withdrawal commands sign through the local OS keyring and can withdraw all available claimable reward buckets.

Mitigation: Before broadcasting, confirm the key name, resolved wallet address, chain ID, node URL, gas settings, and intent to withdraw all claimable rewards.

Risk: Wallet recovery may require sensitive secret material outside the agent workflow.

Mitigation: Do not paste a recovery phrase into chat; perform recovery only in a trusted terminal or official wallet flow.

## Reference(s):

- [Init Setup](references/init-setup.md)
- [OpenMath Reward Claim Reference](references/reward_claim_flow.md)
- [OpenMath Portal](https://openmath.shentu.org)
- [ClawHub Skill Page](https://clawhub.ai/bennyzhe/skills/openmath-claim-reward)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Shentu CLI query or withdrawal commands; withdrawal guidance requires explicit confirmation of the key name, wallet address, chain ID, node URL, and gas settings before signing.]

## Skill Version(s):

v1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
