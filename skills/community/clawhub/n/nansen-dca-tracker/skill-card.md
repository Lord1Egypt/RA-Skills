## Description: <br>
Tracks Solana tokens that whales and smart-money wallets are dollar-cost averaging into, with commands for Jupiter DCA strategies and target token fundamentals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and market researchers use this skill to query Nansen CLI data about Solana DCA activity, token fundamentals, and fund-flow signals for smart-money and whale wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on nansen-cli and a Nansen API key, so local command execution relies on a trusted CLI package and careful credential handling. <br>
Mitigation: Install only if you trust the nansen-cli package and provide the API key through the documented NANSEN_API_KEY environment variable. <br>
Risk: Generated nansen commands outside the documented research examples may query broader market data than intended. <br>
Mitigation: Review each generated nansen command before approving execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-dca-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires nansen-cli and NANSEN_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
