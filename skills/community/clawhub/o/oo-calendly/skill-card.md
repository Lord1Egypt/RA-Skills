## Description: <br>
Calendly (calendly.com) supports reading, creating, updating, and deleting Calendly data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to operate Calendly through an OOMOL-connected account, including reading scheduling data and performing confirmed booking, webhook, organization, and event-management actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform write and destructive Calendly actions, including booking, cancellation, webhook, invitation, and membership changes. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before running write actions, and require explicit approval before destructive actions. <br>
Risk: The skill requires OAuth-connected Calendly credentials and uses sensitive account access through OOMOL. <br>
Mitigation: Install and use it only in trusted environments with the intended authenticated account, and reconnect or refresh credentials only when an action fails for an auth or connection reason. <br>
Risk: Server security guidance says to install this only where ClawHub maintainer tooling is appropriate. <br>
Mitigation: Review the skill and its command behavior before deployment, and limit use to trusted repo and account contexts. <br>


## Reference(s): <br>
- [Calendly homepage](https://calendly.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-calendly) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns Calendly connector responses as JSON when commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
