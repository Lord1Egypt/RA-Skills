## Description: <br>
Automated refactoring assistant. Performs safe code transformations including rename, extract method, inline variable, and move code. Provides refactoring suggestions and performs batch operations with preview and undo support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Python code for refactoring opportunities, preview symbol renames, apply supported rename operations, and restore files from generated backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite or restore many project files. <br>
Mitigation: Run it inside a Git repository, inspect previews with --dry-run before executing changes, and review the resulting diff before committing. <br>
Risk: Documented behavior does not fully match implemented support for extract, inline, move, batch, preview-by-default, ignore configuration, and JavaScript workflows. <br>
Mitigation: Verify implementation support before relying on those documented workflows and limit use to the implemented Python rename, suggest, undo, and backup listing commands. <br>
Risk: Undo restores backup files and can overwrite current project files. <br>
Mitigation: Prefer explicit backup IDs for undo operations and avoid pointing the skill at broad workspace or home directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/openclaw-refactoring) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, refactoring suggestions, and code file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create backup files under .refactoring/backup when rename operations are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
