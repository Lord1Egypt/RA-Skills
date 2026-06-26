## Description: <br>
Migrate OpenClaw agents across platforms and servers, preserving identity, memory, configuration, skills, and extensions for deployment, backup, syncing, and upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haha8d](https://clawhub.ai/user/haha8d) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to migrate, back up, restore, or synchronize OpenClaw agent state between local, remote, development, production, and containerized environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration and sync workflows can upload sensitive agent data, including memory, identity, configuration, and custom skills. <br>
Mitigation: Use only trusted private repositories, inspect backup contents before pushing, and manually check configuration templates for secrets. <br>
Risk: Restore operations can overwrite existing OpenClaw files on the target environment. <br>
Mitigation: Back up the target .openclaw directory first or restore into a staging directory before replacing production agent state. <br>
Risk: Force-push synchronization can replace remote backup history. <br>
Mitigation: Avoid the force-push path unless the remote repository state has been reviewed and replacement is intentional. <br>


## Reference(s): <br>
- [Openclaw Migrate on ClawHub](https://clawhub.ai/haha8d/openclaw-migrate-2) <br>
- [Docker deployment guide](artifact/references/docker-deploy.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and migration workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce backup archives, restore scripts, Git repository updates, and Docker deployment configuration when the referenced scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
