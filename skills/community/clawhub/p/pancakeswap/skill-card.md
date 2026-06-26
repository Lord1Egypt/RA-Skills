## Description: <br>
Audit PancakeSwap liquidity positions before capital is deployed by evaluating depth, concentrated-liquidity setup, range risk, pool quality, and approval friction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Duclawbot](https://clawhub.ai/user/Duclawbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External DeFi users and liquidity providers use this skill to review PancakeSwap pools and LP position structures before committing capital. It supports pool-depth, range-risk, fee-tier, and structure checks for deploy, widen, reduce, monitor, or avoid decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's output could be mistaken for financial advice, guaranteed yield, or a smart-contract audit. <br>
Mitigation: Treat the output as decision support and verify live pool data, token risk, market assumptions, and smart-contract safety before deploying capital. <br>
Risk: Missing or stale pool context can lead to overconfident LP recommendations. <br>
Mitigation: Require pool pair, chain, version, fee tier, intended size, intended range, and current depth or volume context before relying on the assessment. <br>


## Reference(s): <br>
- [PancakeSwap Skill Release](https://clawhub.ai/Duclawbot/pancakeswap) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/Duclawbot) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown assessment with structured risk findings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decision-support output only; no wallet, contract, or trade execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
