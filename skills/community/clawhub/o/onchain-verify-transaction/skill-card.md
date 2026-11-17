## Description:

Verify EVM transaction calldata via Tenderly before signing by confirming token movements, amounts, and recipient addresses as a pre-execution safety gate for other skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougalcantara](https://clawhub.ai/user/dougalcantara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before sending EVM transactions to simulate calldata with Tenderly and compare resulting token and native asset changes against the user's stated intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is used as a financial transaction safety gate, and the security summary says its approval checks are under-specified and could miss dangerous permissions.

Mitigation: Review the skill before relying on it for real transactions and require stronger approval and authorization-state checks, especially for token approvals, Permit or Permit2, NFT operator approvals, multicalls, and proxy-mediated calls.

Risk: Verification may be unavailable when the Tenderly access key is missing, a chain is unsupported, Tenderly returns an error, or rate limits are reached.

Mitigation: Treat unavailable verification as a failure path, surface the condition clearly, and require explicit user confirmation before proceeding without verification.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dougalcantara/skills/onchain-verify-transaction)
- [Tenderly](https://tenderly.co)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash and JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TENDERLY_NODE_ACCESS_KEY and supports the EVM chain IDs listed in the skill.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
