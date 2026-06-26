## Description: <br>
Portal helps agents use the PKU campus information portal CLI for free-classroom lookup, academic calendar lookup, network-fee status checks, low-balance monitoring, and user-approved recharge flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query PKU campus portal information, inspect network-fee balance and sessions, monitor low balance, and prepare recharge commands with explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use PKU ITS credentials and stored portal sessions. <br>
Mitigation: Treat credentials and files under ~/.config/info/portal/ as sensitive, and clear stored sessions when they are no longer needed. <br>
Risk: The skill can start a real network-fee recharge flow. <br>
Mitigation: Require explicit user approval of the recharge amount and payment method before running any recharge command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wjsoj/pku-portal) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide commands that access PKU portal services, use stored credentials, or initiate user-approved network-fee recharge flows.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
