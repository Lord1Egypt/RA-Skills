## Description: <br>
Analyze perpetual futures positions directly in Claude Code - liquidation price, risk/reward, PnL, and probability-based trade plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[farisalahmad714](https://clawhub.ai/user/farisalahmad714) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and traders use this skill to analyze perpetual futures setups from natural-language trade parameters. It calls the Perpulator API to calculate liquidation price, risk/reward, PnL, and related risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trade setup details are sent to the Perpulator API. <br>
Mitigation: Use only with trade data you are comfortable sending to Perpulator and review the service's privacy and retention practices. <br>
Risk: The skill uses a PERPULATOR_API_KEY from the environment, and the key-check command may print it in shared terminals or logs. <br>
Mitigation: Use a dedicated or limited API key where possible and avoid exposing terminal output or logs that may contain the secret. <br>
Risk: Leverage and liquidation analysis can inform high-risk trading decisions. <br>
Mitigation: Treat outputs as calculation support, review all assumptions, and make independent trading decisions. <br>


## Reference(s): <br>
- [Perpulator Homepage](https://perpulator.vercel.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/farisalahmad714/perpulator) <br>
- [Publisher Profile](https://clawhub.ai/user/farisalahmad714) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and PERPULATOR_API_KEY; sends trade setup details to the Perpulator API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
