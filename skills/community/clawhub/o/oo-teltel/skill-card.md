## Description: <br>
TelTel lets an agent operate a TelTel account through OOMOL's oo CLI for account balance checks, SMS delivery reports, and single outbound SMS sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to perform TelTel account and SMS workflows from an agent while relying on OOMOL-connected credentials. Read actions cover balances and delivery reports; the write action sends one outbound SMS after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real outbound SMS messages that may reach external recipients and incur costs. <br>
Mitigation: Confirm the recipient, message body, and expected effect with the user before allowing any send_sms action. <br>
Risk: The skill requires access to a connected TelTel account and related credentials. <br>
Mitigation: Install only when OOMOL's oo CLI and a connected TelTel account are intended for use; rely on OOMOL-managed credential injection rather than handling raw tokens. <br>


## Reference(s): <br>
- [ClawHub TelTel Skill](https://clawhub.ai/oomol/oo-teltel) <br>
- [TelTel Homepage](https://www.teltel.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected TelTel account through OOMOL; SMS sending may incur external communication costs.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
