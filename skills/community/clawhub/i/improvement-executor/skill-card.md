## Description: <br>
Applies approved improvement candidates to target files, creates backups, and supports rollback for Markdown and YAML frontmatter changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill after candidate scoring to apply accepted documentation or frontmatter changes and produce execution artifacts for gate checks or rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The executor can overwrite local files based on target paths supplied in ranking artifacts. <br>
Mitigation: Inspect target_path and the selected candidate action before execution, and run the skill only in a workspace where those paths are expected to be writable. <br>
Risk: The documented execute.py preview mode is not implemented in the artifact. <br>
Mitigation: Do not rely on execute.py --dry-run; review the candidate plan and run against a copy or disposable workspace before applying changes to important files. <br>
Risk: Using --force bypasses the acceptance gate and can apply candidates that were not accepted for execution. <br>
Mitigation: Avoid --force unless a human reviewer has intentionally approved the exact candidate and action. <br>
Risk: Rollback depends on receipt and backup artifacts remaining accurate and available. <br>
Mitigation: Preserve generated execution, receipt, and backup files until the change has passed review, and inspect rollback pointers before restoring files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/improvement-executor) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/lanyasheng) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, json, file edits, markdown, configuration] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON execution or rollback artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can modify local target files and create backup, execution, receipt, and rollback artifacts.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
