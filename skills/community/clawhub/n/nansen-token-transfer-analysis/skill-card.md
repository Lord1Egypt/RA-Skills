## Description: <br>
Where is this token moving and why? Large transfers, flow trends over time, and breakdown by wallet label. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to investigate token movement, large transfers, flow trends, and wallet-label breakdowns through Nansen CLI research commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Nansen API key. <br>
Mitigation: Install and use it only where the agent is allowed to access NANSEN_API_KEY, and avoid exposing the key in prompts, logs, or shared output. <br>
Risk: The skill depends on the nansen-cli package and permits Nansen CLI commands. <br>
Mitigation: Use it only if you trust the nansen-cli package source, keep usage to the documented token research commands, and review commands before execution. <br>
Risk: Token flow analysis can fail for stablecoins. <br>
Mitigation: Use non-stablecoin token addresses for token flows, and skip the flow command for stablecoin tokens as documented by the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nansen-devops/nansen-token-transfer-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/nansen-devops) <br>
- [nansen-cli package](https://www.npmjs.com/package/nansen-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise analytical guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; token flow analysis excludes stablecoins.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
