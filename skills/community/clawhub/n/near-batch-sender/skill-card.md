## Description: <br>
Batch operations for NEAR tokens - send to multiple recipients, transfer NFTs, claim rewards with cost estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and NEAR operators use this skill to prepare and run batch NEAR token sends, NFT transfers, reward or airdrop claim workflows, and pre-execution cost estimates from JSON input files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move NEAR tokens and NFTs in bulk, so an incorrect or untrusted JSON input file can cause unwanted asset transfers. <br>
Mitigation: Inspect every JSON input file before use, run testnet or very small trials first, and confirm the recipient accounts, token IDs, NFT contracts, and amounts before executing transfers. <br>
Risk: The security summary notes weak safeguards around input files and command execution. <br>
Mitigation: Use the skill only when you fully trust it, avoid untrusted recipient or NFT files, and prefer argument-based process execution, input validation, and an explicit pre-transfer review or confirmation flow before production use. <br>


## Reference(s): <br>
- [NEAR CLI](https://docs.near.org/tools/near-cli) <br>
- [NEAR Batch Actions](https://docs.near.org/api/rpc/transactions/batch-actions) <br>
- [ClawHub skill page](https://clawhub.ai/shaiss/near-batch-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces batch-operation instructions, JSON input shapes, cost-estimation guidance, and command-line usage for NEAR CLI workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
