## Description: <br>
Converts Markdown, text, Word, PDF, HTML, and RTF inputs into .docx documents formatted for Chinese government document standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wisink](https://clawhub.ai/user/Wisink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and document-preparation agents use this skill to convert reports, policy analyses, work summaries, and training materials into strictly formatted government-style .docx files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter reads local source documents and writes a local .docx file. <br>
Mitigation: Run it only on documents intended for conversion and keep sensitive inputs within the user's approved local workspace. <br>
Risk: Supplying an existing output path can overwrite important work. <br>
Mitigation: Choose a new or disposable output filename before running the conversion command. <br>
Risk: Optional parsers for PDF, HTML, RTF, and Word formats depend on local Python packages. <br>
Mitigation: Install dependencies only from trusted package sources and keep the environment scoped to this conversion task. <br>


## Reference(s): <br>
- [Government Document Format Rules](references/format-rules.md) <br>
- [Conversion Lessons Learned](references/lessons-learned.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; generated .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local .docx output path supplied by the user.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
