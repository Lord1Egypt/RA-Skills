## Description: <br>
Convert Markdown files to PDF with LaTeX math rendering and CJK support using Pandoc and XeLaTeX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaruoji](https://clawhub.ai/user/huaruoji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and technical writers use this skill to convert trusted Markdown reports, notes, or documentation into printable PDFs with math, code blocks, tables, and mixed CJK/Latin text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pandoc and XeLaTeX may process raw LaTeX or local-file references when converting hostile Markdown. <br>
Mitigation: Use the skill only with trusted Markdown and trusted option values, and review source documents before conversion. <br>
Risk: Required conversion tools and TeX packages run locally and affect the generated output. <br>
Mitigation: Install Pandoc, XeLaTeX, TeX Live packages, and fonts only from trusted package sources. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/huaruoji/md2pdf-xelatex) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown with inline bash commands and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Pandoc, XeLaTeX, TeX Live packages, and suitable fonts for CJK output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
