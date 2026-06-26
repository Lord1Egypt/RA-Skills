## Description: <br>
SMS Alert (smsalert.co.in). Use this skill for ANY SMS Alert request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate an OOMOL-connected SMS Alert account, including sending SMS messages, generating and validating OTPs, and checking account resources such as balances, sender IDs, and templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected SMS Alert account and may rely on sensitive credentials managed outside the agent. <br>
Mitigation: Use the OOMOL connector flow and avoid exposing raw API tokens in prompts, files, or shell history. <br>
Risk: The send_sms action can send real SMS messages and consume account credit. <br>
Mitigation: Confirm the recipient, message body, sender, and intended effect with the user before running write actions. <br>
Risk: Connector schemas may change over time. <br>
Mitigation: Inspect the live action schema with oo connector schema before constructing each payload. <br>


## Reference(s): <br>
- [SMS Alert homepage](https://www.smsalert.co.in/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
