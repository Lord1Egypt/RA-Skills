## Description: <br>
音乐文件批量标签工具，支持读取/编辑音乐元数据（歌名、艺术家、专辑、流派等），批量编辑标签，按标签整理音乐文件，预览模式和撤销功能！ <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and end users can use this skill as a local command-line workflow for inspecting, previewing, batch tagging, organizing, and undoing music file organization tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool presents tag editing and tag-based organization as usable, while the current implementation simulates tag reads and writes. <br>
Mitigation: Verify behavior on expendable test files before relying on edits or organization results. <br>
Risk: Batch organize and undo workflows can copy or remove local files based on generated mappings. <br>
Mitigation: Use preview mode first and keep separate backups before running batch or organize commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/music-tagger) <br>
- [Publisher Profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output with shell command examples and file organization guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file operations may copy or remove files during organize and undo commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-03-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
