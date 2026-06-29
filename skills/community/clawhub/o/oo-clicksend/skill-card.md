## Description: <br>
Enables agents to operate ClickSend through the OOMOL `oo` CLI for account lookup, SMS pricing and sending, contact list management, and contact management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent perform ClickSend account, SMS, contact list, and contact operations through an OOMOL-connected account while inspecting live action schemas before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send SMS messages, update contacts, and delete ClickSend data, which can cost money, message real recipients, or remove business data. <br>
Mitigation: Review and explicitly approve SMS sends, contact updates, and destructive actions before execution. <br>
Risk: The skill depends on OOMOL-connected ClickSend credentials and the remote `oo` CLI setup path. <br>
Mitigation: Install and connect OOMOL only when the user intends to operate ClickSend through OOMOL, and treat the remote installer as a normal third-party setup step. <br>


## Reference(s): <br>
- [ClickSend Homepage](https://www.clicksend.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-clicksend) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before payload construction; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
