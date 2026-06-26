## Description: <br>
StatusCake connector skill for reading and managing uptime monitoring resources through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect and manage StatusCake uptime tests, monitoring locations, alerts, probe history, and uptime or downtime periods from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete StatusCake monitoring data. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before running write or destructive actions. <br>
Risk: The skill requires sensitive account credentials through an OOMOL-connected StatusCake account. <br>
Mitigation: Use the OOMOL connection flow and avoid handling raw StatusCake API tokens in prompts, files, or shell history. <br>
Risk: Suggested first-time setup commands install or invoke the oo CLI. <br>
Mitigation: Verify the oo CLI installer source before running curl or PowerShell install commands. <br>


## Reference(s): <br>
- [StatusCake homepage](https://www.statuscake.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-statuscake) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before actions; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
