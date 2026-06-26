## Description: <br>
Convert academic papers into structured Chinese reading reports with original figures. Supports arXiv HTML and local PDF inputs. For arXiv links, HTML mode is preferred for textual accuracy. Use when the user asks to summarize, read, analyze, or create a reading report for an academic paper (PDF file or arXiv link). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuaalixu](https://clawhub.ai/user/nuaalixu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and students use this skill to turn academic papers from arXiv HTML pages or local PDFs into structured Chinese reading reports with selected original figures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download paper pages or images from user-provided URLs and process local PDFs. <br>
Mitigation: Review URLs and PDF paths before use, use trusted sources, and avoid private papers unless local extraction is acceptable. <br>
Risk: The skill writes extracted text, figures, and generated reports in the workspace. <br>
Mitigation: Run it in an appropriate workspace and review generated files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nuaalixu/paper-report) <br>
- [HTML reader workflow](reader/html.md) <br>
- [PDF reader workflow](reader/pdf.md) <br>
- [HTML writer workflow](writer/html.md) <br>
- [Markdown writer workflow](writer/markdown.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese reading report in self-contained HTML or Markdown, with extracted figure files when Markdown output is selected] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local paper, page, figure, and report files in the workspace.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
