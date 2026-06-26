## Description: <br>
Create and redeem Linkdrop claim links from the command line with strict JSON output on Base, Polygon, Arbitrum, Optimism, and Avalanche. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seichris](https://clawhub.ai/user/seichris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to create funded Linkdrop claim links, redeem claim links to destination addresses, and consume one JSON object per CLI invocation for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can sign and broadcast real blockchain transactions from a private key without a built-in confirmation step. <br>
Mitigation: Use a dedicated, low-balance wallet and review the amount, token, chain, destination, and claim URL before every run. <br>
Risk: Runtime secrets include a wallet private key, a Linkdrop API key, and RPC URLs. <br>
Mitigation: Keep secrets out of logs, repositories, and shared shell history; avoid using a primary wallet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seichris/linkdrop-agent-cli) <br>
- [Linkdrop SDK CLI Homepage](https://github.com/seichris/linkdrop-sdk-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON objects from the CLI with markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Success responses include fields such as claimUrl, transferId, depositTx, and redeemTx; failures return ok: false with an error object.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
