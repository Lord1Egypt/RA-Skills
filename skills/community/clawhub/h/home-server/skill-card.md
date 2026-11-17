## Description:

Plan, secure, and maintain a home server with Docker services, remote access, backups, and incident recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Home server operators and developers use this skill to plan Docker-based services, classify exposure boundaries, document backup coverage, and work through operational incidents and recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may keep persistent local notes about a home-server environment in ~/home-server/.

Mitigation: Create or update those notes only after user confirmation, avoid storing secrets, and choose narrow activation preferences if broad Docker or networking assistance is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/home-server)
- [Skill Homepage](https://clawic.com/skills/home-server)
- [Setup - Home Server](artifact/setup.md)
- [Memory Template - Home Server](artifact/memory-template.md)
- [Service Catalog Template](artifact/service-catalog.md)
- [Operations Checklists](artifact/operations-checklists.md)
- [Incident Playbook](artifact/incident-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, structured notes, and adaptable command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local notes under ~/home-server/ only after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
