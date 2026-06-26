## Description: <br>
Converts Markdown files to Word .docx documents with Pandoc, then applies Chinese font settings and table borders with python-docx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sukimgit](https://clawhub.ai/user/sukimgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation authors, and agents use this skill to convert Markdown documents or directories of Markdown files into Word documents for sharing, reports, academic drafts, meeting notes, and Chinese-language official-document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter reads input Markdown files, writes output .docx files, creates parent output directories, and can recursively process a directory. <br>
Mitigation: Use explicit input and output paths, review directories before batch conversion, and avoid running recursive conversion over untrusted or overly broad paths. <br>
Risk: Conversion depends on executing the local Pandoc binary and importing python-docx. <br>
Mitigation: Install Pandoc and python-docx from trusted sources and keep them updated according to local package-management policy. <br>
Risk: The template helper writes to a hard-coded Windows path. <br>
Mitigation: Run the helper only when that exact template output location is intended, or adjust the path before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sukimgit/md2docx) <br>
- [Publisher profile](https://clawhub.ai/user/sukimgit) <br>
- [Pandoc installation guide](https://pandoc.org/installing.html) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python examples; runtime output is Word .docx files and conversion status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pandoc and python-docx; accepts Markdown input paths, Word output paths, optional template or reference document paths, and optional recursive directory conversion.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
