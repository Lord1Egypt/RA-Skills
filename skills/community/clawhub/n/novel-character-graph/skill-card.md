## Description: <br>
Analyzes long-form novels, extracts character systems and relationship maps, creates interactive HTML graph outputs, and helps draft theme-song prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengbin92](https://clawhub.ai/user/mengbin92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process large TXT, EPUB, PDF, DOCX, or MOBI novels into character rosters, relationship maps, worldbuilding summaries, timelines, and visualization files. It can also guide theme-song, ending-song, OST, and related media-prompt creation from novel context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose dependency installation or privileged system package setup. <br>
Mitigation: Require explicit user confirmation before package installation or any sudo command, and prefer already-installed tools where possible. <br>
Risk: Generated HTML may include content derived from untrusted novel text. <br>
Mitigation: Keep outputs in a dedicated folder and review or open generated HTML in an isolated browser context before sharing or reusing it. <br>
Risk: Media processing and file generation can overwrite local files. <br>
Mitigation: Require confirmation before ffmpeg runs or local file overwrites, and write outputs to a dedicated destination path. <br>


## Reference(s): <br>
- [Novel Format Processing Handbook](references/format_handbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mengbin92/novel-character-graph) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, Python helper scripts, and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce multiple local deliverables, including Markdown reports and an interactive HTML character graph.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
