## Description: <br>
Teaches the agent how to list, inspect, diff, and restore Plakar snapshots when a user asks to undo, roll back, restore, or revert files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misterflop](https://clawhub.ai/user/misterflop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to recover files from Plakar snapshots after a bad edit, rollback request, or restore request. It guides snapshot listing, inspection, diffing, and user-confirmed restore operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore commands can overwrite live files if the wrong snapshot, path, or destination is selected. <br>
Mitigation: Confirm the backup store, snapshot ID, files or paths, and destination before restore; prefer restoring to a temporary directory when practical. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Plakar store and user confirmation before restore commands that may overwrite live files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
