## Description: <br>
Converts Markdown text or files into PDF documents with custom styling and code syntax highlighting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alone86136](https://clawhub.ai/user/alone86136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and other users can use this skill to convert Markdown documentation, notes, reports, or shareable content into PDF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PDF renderer can access local files while converting Markdown. <br>
Mitigation: Convert only trusted Markdown and CSS, or run the skill in a sandbox with tightly limited filesystem access. <br>
Risk: Untrusted Markdown may cause local file contents to appear in the generated PDF. <br>
Mitigation: Avoid processing documents from other people unless local file access is removed or constrained before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alone86136/markdown-to-pdf) <br>
- [Publisher profile](https://clawhub.ai/user/alone86136) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PDF file output with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires markdown and pygments Python packages plus the wkhtmltopdf system binary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
