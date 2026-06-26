## Description: <br>
Backup/restore OpenClaw config and workspace via git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[burnlife001](https://clawhub.ai/user/burnlife001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to back up and restore OpenClaw configuration and workspace directories through Git repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup flow can push broad OpenClaw configuration and workspace data to an external Git remote. <br>
Mitigation: Before running backup commands, edit config.sh so the Git host and organization point only to repositories you control, inspect every configured backup path, and review .gitignore for secrets and private workspace files. <br>
Risk: The restore flow can delete local files or overwrite local state when restoring into existing directories. <br>
Mitigation: Make a separate local copy before restoring, test each target in a temporary directory, and avoid restore.sh all until every configured target has been checked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/burnlife001/openclaw-gitbak) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill points agents to bash scripts that read scripts/config.sh and operate on configured local paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
