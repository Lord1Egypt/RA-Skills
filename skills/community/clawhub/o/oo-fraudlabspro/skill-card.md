## Description: <br>
FraudLabs Pro (fraudlabspro.com). Use this skill for ANY FraudLabs Pro request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate FraudLabs Pro through an OOMOL-connected account, including screening orders, retrieving order screening results, and submitting approve or reject feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run write actions that affect FraudLabs Pro order screening and feedback records. <br>
Mitigation: Require clear user intent and confirm the exact payload and expected effect before running write actions such as screen_order, get_order_result, or feedback_order. <br>
Risk: The skill requires a connected FraudLabs Pro account and sensitive credentials managed through OOMOL. <br>
Mitigation: Install it only for users who intend the agent to work with their FraudLabs Pro account and review the connected account permissions before use. <br>
Risk: Broad activation wording may cause the skill to be selected for more FraudLabs Pro-related tasks than intended. <br>
Mitigation: Require explicit user intent before actions that affect fraud decisions, order feedback, customer verification, or reseller/account changes. <br>


## Reference(s): <br>
- [FraudLabs Pro homepage](https://www.fraudlabspro.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-fraudlabspro) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before running FraudLabs Pro actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
