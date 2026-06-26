## Description: <br>
Convert Markdown files with slide separators into PowerPoint (PPTX) presentations, saving to an active Obsidian vault by default when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhcanyu4](https://clawhub.ai/user/zhcanyu4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and knowledge workers use this skill to turn Markdown slide drafts into PPTX presentations, including Markdown files separated by --- slide delimiters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PPTX files are saved to the active Obsidian vault by default when no output path is provided. <br>
Mitigation: Provide an explicit output path when the presentation should be written somewhere else. <br>
Risk: Conversion depends on local LibreOffice or Pandoc executables found on PATH. <br>
Mitigation: Use trusted local installations of LibreOffice or Pandoc before running conversion commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands that produce a PPTX file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create an intermediate HTML file and writes PPTX output to the active Obsidian vault by default, or to a caller-specified path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
