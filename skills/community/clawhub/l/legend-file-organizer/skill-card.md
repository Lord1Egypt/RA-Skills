## Description: <br>
File Organizer helps agents plan safe file organization and batch workspace operations, including moving files, batch renaming, directory scaffolding, grouping by type or date, and restructuring project layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougchambes](https://clawhub.ai/user/dougchambes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace users use this skill when they need an agent to propose predictable file moves, renames, directory structures, and cleanup steps while preserving review points before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch file moves or renames can affect many files at once if the matched set or destination is wrong. <br>
Mitigation: Preview the matched files and planned commands first, confirm destination directories, and keep a backup or git checkpoint before major restructures. <br>
Risk: Deletion examples for empty files or directories can remove disposable-looking items that the user still needs. <br>
Mitigation: Require explicit approval for delete commands and confirm the matched files or empty directories are truly disposable before execution. <br>
Risk: Workspace organization commands can operate outside the intended boundary if paths are not checked. <br>
Mitigation: Confirm the target directory before approval and keep operations within the intended workspace. <br>


## Reference(s): <br>
- [File Organization Patterns](references/patterns.md) <br>
- [File Organizer release page](https://clawhub.ai/dougchambes/legend-file-organizer) <br>
- [Publisher profile](https://clawhub.ai/user/dougchambes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples and directory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; command execution remains subject to user review and approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
