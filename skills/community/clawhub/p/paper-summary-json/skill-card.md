## Description: <br>
Analyzes academic papers from local files or direct URLs, extracts structured evidence-backed JSON, verifies claims against the source text, and renders Markdown, HTML, and DOCX reports in Chinese or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crw0149](https://clawhub.ai/user/crw0149) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to turn PDF, DOCX, text, Markdown, or HTML papers into structured paper summaries with evidence spans, consistency checks, and editable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided papers and derived prompts, JSON, and reports are stored locally on the Desktop by default. <br>
Mitigation: Use an appropriate output directory for sensitive work and delete generated batches when they are no longer needed. <br>
Risk: Paper content may be sent to the selected model provider during extraction and verification. <br>
Mitigation: Avoid confidential, unpublished, regulated, or copyright-sensitive papers unless the model provider's data handling is acceptable. <br>


## Reference(s): <br>
- [Prompt templates](references/prompt_templates.md) <br>
- [Workflow mapping](references/workflow_mapping.md) <br>
- [ClawHub skill page](https://clawhub.ai/crw0149/paper-summary-json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [JSON extraction and verification files, Markdown/HTML/DOCX reports, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime files are saved under ~/Desktop/paper_analysis_results/<YYYYMMDD_HHMMSS>/ by default unless the user chooses another output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
