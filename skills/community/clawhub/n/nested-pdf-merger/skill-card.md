## Description: <br>
Use this skill when the task is to merge PDFs from a nested directory tree into a single PDF with hierarchical bookmarks by invoking the external `nestedpdfmerger` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lyutenant](https://clawhub.ai/user/Lyutenant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to merge PDFs from a nested folder tree into a single output PDF while preserving folder hierarchy as bookmarks. It also guides previewing merge order, excluding directories, sorting inputs, and handling missing CLI installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external PDF-merging CLI against local files, so the selected input directory and output path determine which documents are read and written. <br>
Mitigation: Provide explicit input and output paths, confirm the intended directory, and use `--dry-run` before merging when order or sensitive documents matter. <br>
Risk: The required `nestedpdfmerger` binary may be absent or may not be the intended installed package. <br>
Mitigation: Verify the pip package before installation and confirm `nestedpdfmerger` is available on PATH before running merge commands. <br>


## Reference(s): <br>
- [Nested PDF Merger project homepage](https://github.com/Lyutenant/nested-pdf-merger) <br>
- [ClawHub release page](https://clawhub.ai/Lyutenant/nested-pdf-merger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose dry-run commands before merging PDFs and installation guidance when the required binary is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
