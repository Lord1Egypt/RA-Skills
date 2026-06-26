## Description: <br>
Defines the Pet-Game mini-program workflow for pre-edit file backups, element snapshot tracking, and post-commit backup cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marszxf](https://clawhub.ai/user/marszxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators maintaining the Pet-Game mini-program use this skill to enforce a backup-first workflow, track repeated element adjustments, and clean backups after commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad activation scope for file edits and Git commits. <br>
Mitigation: Enable it only for the intended Pet-Game workspace and review when backup commands should run. <br>
Risk: The cleanup behavior can delete backup snapshots after commits. <br>
Mitigation: Confirm the backup directory, retention policy, and whether cleanup supports a dry run or confirmation before routine use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marszxf/pet-game-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/marszxf) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies local backup and cleanup workflow rules to agent file-editing and Git commit activity.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
