## Description: <br>
Operates Elorus through an OOMOL-connected account so an agent can read, create, and update contacts, invoices, and products or services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and developers can use this skill to have an agent list, inspect, create, and update Elorus contacts, invoices, and products or services through the OOMOL connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update Elorus contacts, invoices, and products or services. <br>
Mitigation: Require user confirmation of the exact payload and intended effect before approving any write action. <br>
Risk: The skill depends on a connected OOMOL account and server-side connector credentials. <br>
Mitigation: Install and use it only when OOMOL handling connector credentials is acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-elorus) <br>
- [Elorus Homepage](https://www.elorus.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL Elorus Connection](https://console.oomol.com/app-connections?provider=elorus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live connector schema inspection before constructing payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
