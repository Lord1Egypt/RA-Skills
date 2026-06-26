## Description: <br>
Guides agents through planning MillionFinneyHomepage pixel art, preparing IPFS media, and understanding the Ethereum contract claiming process without automatic transaction execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l0c0luke](https://clawhub.ai/user/l0c0luke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, artists, and agent operators use this skill to understand how to prepare pixel artwork, map it onto the MillionFinneyHomepage grid, upload media to IPFS, and review the contract interactions required for pixel claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real wallet signing or ETH spending could occur if a user follows contract guidance without review. <br>
Mitigation: Keep transaction approval user-controlled, inspect the exact signature text, and use a limited or burner wallet when possible. <br>
Risk: Incorrect domain, contract address, or pixel coordinates could cause failed uploads, wrong transactions, or irreversible on-chain records. <br>
Mitigation: Verify the official domain and contract address, re-check pixel availability before purchase, and test with small claims first. <br>
Risk: Secrets may be exposed if private keys or API keys are pasted into chat or shared with an agent. <br>
Mitigation: Never paste private keys into chat and keep API keys private; use local wallet tooling and provider-specific secret handling. <br>
Risk: The helper script writes JSON or CSV files to user-selected paths. <br>
Mitigation: Choose output paths deliberately and review generated payload files before using them for purchases. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/l0c0luke/millionfinney-homepage) <br>
- [Million Finney Homepage Contract Reference](references/contract.md) <br>
- [Pixel Pattern and Artwork Recipes](references/pixel-art.md) <br>
- [Million Finney Homepage IPFS Upload API](https://millionfinneyhomepage.com/api/ipfs/upload) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code snippets, command examples, and optional JSON or CSV pixel payload files from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script can emit pixel payload JSON and optional CSV files for user review before any transaction.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
