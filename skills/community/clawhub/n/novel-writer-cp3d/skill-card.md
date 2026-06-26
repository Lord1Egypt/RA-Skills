## Description: <br>
Comprehensive novel writing assistant for creating, managing, formatting, checking, and converting novel chapters while tracking characters and plot arcs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, editors, and agent users use this skill to draft and continue novel chapters, maintain character and plot consistency, check chapter formatting, and convert Markdown chapters to plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Markdown-to-TXT conversion script writes a .txt output file and may overwrite an existing target path. <br>
Mitigation: Choose and review the output path before running conversions, and keep backups of important manuscript files. <br>
Risk: The skill text references a compile_novel.py script that is not present in the artifact. <br>
Mitigation: Do not rely on that compile capability unless the publisher supplies the missing script or an equivalent reviewed workflow. <br>
Risk: The skill reads and creates local files in a novel workspace. <br>
Mitigation: Use it only in the intended novel workspace and review proposed file changes before accepting them. <br>


## Reference(s): <br>
- [Character Management Guide](references/characters.md) <br>
- [Plot Management Guide](references/plot.md) <br>
- [Novel Writing Style Guide](references/writing_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown prose, plain text manuscript output, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify chapter files and converted text files in a user-selected novel folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
