## Description: <br>
Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronpancn](https://clawhub.ai/user/aaronpancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users can use this skill to inspect, create, validate, proofread, and modify Word, Excel, and PowerPoint files through officecli commands. It is suited for workflows that need structured document reads, targeted edits, live preview, or generated Office artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install instructions run remote shell scripts from officecli.ai without integrity checks. <br>
Mitigation: Review the installer source and trust the download endpoint before installing; prefer a versioned release, package manager, checksum, or signature when available. <br>
Risk: The skill can modify Office files and its watch or resident modes start local helper services. <br>
Mitigation: Use it only on documents intended for inspection or modification, close watch/resident sessions when finished, and validate or review changed files before relying on them. <br>


## Reference(s): <br>
- [Officecli ClawHub skill page](https://clawhub.ai/aaronpancn/skills/officecli) <br>
- [officecli macOS/Linux installer](https://d.officecli.ai/install.sh) <br>
- [officecli Windows installer](https://d.officecli.ai/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline shell commands and optional text or JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify .docx, .xlsx, and .pptx files; watch and resident modes can start local helper services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
