## Description: <br>
Claims earned rewards from the OpenMath platform. Use when the user wants to query claimable imported/proof rewards or withdraw verified Shentu rewards after a proof has passed verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bennyzhe](https://clawhub.ai/user/bennyzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenMath users and developers use this skill to check claimable imported or proof rewards and prepare Shentu reward withdrawals after verifying the reward address, local key, chain ID, and RPC node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A withdrawal command can sign and broadcast a transaction with the local OS keyring. <br>
Mitigation: Before broadcasting, verify the exact shentud binary, reward address, key name, chain ID, and RPC node, and proceed only after the user confirms they match the intended wallet. <br>
Risk: Reward queries and transaction checks depend on the selected Shentu RPC endpoint. <br>
Mitigation: Use a trusted RPC node and confirm any SHENTU_NODE_URL or command-line node override before relying on results or broadcasting. <br>
Risk: Missing or stale OpenMath config can point the flow at the wrong reward address. <br>
Mitigation: Use an explicit address or verify the prover_address loaded from --config, OPENMATH_ENV_CONFIG, or the standard openmath-env.json locations before querying or withdrawing. <br>


## Reference(s): <br>
- [Init Setup](references/init-setup.md) <br>
- [OpenMath Reward Claim Reference](references/reward_claim_flow.md) <br>
- [OpenMath Platform](https://openmath.shentu.org) <br>
- [Default Shentu RPC Endpoint](https://rpc.shentu.org:443) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query a Shentu RPC endpoint and may prepare withdrawal commands that require local OS keyring signing.] <br>

## Skill Version(s): <br>
v1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
