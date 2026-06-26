## Description: <br>
Bark helps an agent read Bark server information and send Bark notifications through an OOMOL-connected Bark account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Bark from an agent, including inspecting server information and sending single-device, batch, or pre-encrypted push notifications after approval for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Bark account and sensitive credentials handled through the OOMOL connection. <br>
Mitigation: Install only if you are comfortable using the connected Bark account and the disclosed credential flow. <br>
Risk: Notification actions can send messages to Bark devices or explicit device keys. <br>
Mitigation: Confirm the exact payload and intended recipients before any write action is executed. <br>
Risk: The oo CLI installer may run shell or PowerShell commands during setup. <br>
Mitigation: Review the installer command and install guide before running setup on a new machine. <br>


## Reference(s): <br>
- [ClawHub Bark skill page](https://clawhub.ai/oomol/oo-bark) <br>
- [Bark homepage](https://bark.day.app) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
