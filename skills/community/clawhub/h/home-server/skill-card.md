## Description: <br>
Plan, secure, and maintain a home server with Docker services, remote access, backups, and incident recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to plan and operate a home server, including Docker service layout, remote access boundaries, backups, maintenance checks, and incident recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved home-server notes may contain sensitive topology or operational details if the user records too much detail. <br>
Mitigation: Review what is saved in ~/home-server/ and avoid passwords, API keys, private keys, full .env files, or sensitive network details. <br>
Risk: Incorrect service exposure guidance could increase the home network attack surface. <br>
Mitigation: Classify services as LAN-only, VPN-only, or internet-facing before changes, keep admin panels and databases off the public internet, and review proposals before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/home-server) <br>
- [Skill Homepage](https://clawic.com/skills/home-server) <br>
- [Setup - Home Server](setup.md) <br>
- [Memory Template - Home Server](memory-template.md) <br>
- [Service Catalog Template](service-catalog.md) <br>
- [Operations Checklists](operations-checklists.md) <br>
- [Incident Playbook](incident-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with checklists, templates, operational guidance, and adaptable shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local notes under ~/home-server/ only after user confirmation; does not deploy services or open ports automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
