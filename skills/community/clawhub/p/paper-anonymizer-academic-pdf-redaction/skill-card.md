## Description: <br>
Redact text from PDF documents for blind review anonymization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, authors, and reviewers use this skill to redact identifying details from academic PDFs before blind review while preserving references and most original text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect pattern selection may miss identifying information or redact non-identifying content. <br>
Mitigation: Use full names and exact phrases, run redaction on copies of PDFs first, and manually review the output. <br>
Risk: Overbroad redaction can damage the PDF or remove more content than intended. <br>
Mitigation: Avoid page-level or region-level redactions, preserve the References section, and verify page count and retained text after saving. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/paper-anonymizer-academic-pdf-redaction) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code] <br>
**Output Format:** [Markdown with Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; guides exact-match PDF redaction and post-redaction verification rather than directly producing files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
