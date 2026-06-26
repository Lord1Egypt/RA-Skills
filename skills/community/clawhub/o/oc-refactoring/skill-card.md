## Description: <br>
Automated refactoring assistant that performs code transformations including rename, extract method, inline variable, and move code, while providing refactoring suggestions and batch operations with preview and undo support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect code for refactoring opportunities, preview proposed symbol renames, apply supported refactoring changes, and undo changes from generated backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite many project files during refactoring operations. <br>
Mitigation: Run inside version control, use --dry-run first, target a narrow directory, review generated diffs, and keep the .refactoring backups available for rollback. <br>
Risk: The release evidence notes that documented extract, inline, move, and batch behavior may overstate implemented support. <br>
Mitigation: Verify support for the intended operation before relying on it, and avoid assuming advertised behavior works without testing on a small sample. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/oc-refactoring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell commands and code/configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project file modifications and .refactoring backups when execution mode is used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
