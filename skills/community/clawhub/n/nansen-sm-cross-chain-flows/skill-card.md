## Description: <br>
Is SM buying this token on one chain but selling on another? Detect capital rotation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to run Nansen smart-money netflow checks across Ethereum, Solana, Base, and BNB, then compare 24h and 7d flow divergence for potential cross-chain capital rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Nansen CLI research commands and may consume Nansen API quota. <br>
Mitigation: Confirm the user trusts the nansen-cli package, has configured NANSEN_API_KEY intentionally, and is comfortable using API quota before running the commands. <br>
Risk: Interpreting absent token results as lack of support can be misleading. <br>
Mitigation: Treat absent results as possible low smart-money activity on that chain, and focus on 24h and 7d divergence rather than 1h movement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-sm-cross-chain-flows) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY; analyzes netflow windows including 1h, 24h, 7d, and 30d.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
