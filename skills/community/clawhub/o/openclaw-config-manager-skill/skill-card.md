## Description: <br>
Provides OpenClaw configuration backup, restore, migration, Git version control, encryption, and permission management guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wisdom-wozoy](https://clawhub.ai/user/wisdom-wozoy) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to plan and run configuration backups, restores, migrations, Git-based version control, and secret-handling workflows across environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration backups can copy private settings or secrets into Git or other backup storage. <br>
Mitigation: Use a private backup repository, explicit secret exclusions, reviewed encryption, and least-privilege Git credentials before enabling Git backup or auto-push. <br>
Risk: Restore, migration, force-push, sudo, collaborator, or restart operations can overwrite live environments or change access. <br>
Mitigation: Require manual approval, take a fresh backup first, inspect the target files, and keep scheduled auto-push disabled until the backup scope has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wisdom-wozoy/openclaw-config-manager-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include backup, restore, migration, Git, secrets, validation, and troubleshooting commands.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
