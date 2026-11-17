## Description:

Homework Grader helps teachers OCR math answer keys and student homework, compare answers, summarize class error rates, and generate Excel statistics and PDF analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhy123456lhy](https://clawhub.ai/user/lhy123456lhy)

### License/Terms of Use:

MIT-0

## Use Case:

External teachers use this skill to process math answer keys and batches of student homework images, confirm OCR results, grade against the answer key, and produce class-level error analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Student names, answers, homework photos, JSON files, Excel files, and PDFs may contain sensitive student data.

Mitigation: Run the skill in an isolated environment, restrict access to generated files, and delete student data according to school or organizational policy.

Risk: Excel and PDF report generation can carry student-controlled names or answers into files that teachers may trust.

Mitigation: Use trusted inputs only until report generation escapes HTML content and neutralizes spreadsheet formulas.

Risk: Runtime dependencies and OCR tooling may vary across environments.

Mitigation: Pin and verify Python dependencies and the Tesseract OCR installation before deploying the skill for routine classroom use.

## Reference(s):

- [Answer Format](references/answer_format.md)
- [Output Format](references/output_format.md)
- [Tesseract OCR Windows Installer](https://github.com/UB-Mannheim/tesseract/wiki)
- [ClawHub Skill Page](https://clawhub.ai/lhy123456lhy/skills/homework-grader)

## Skill Output:

**Output Type(s):** [Text, JSON, Excel files, PDF files, Guidance]

**Output Format:** [Markdown instructions, OCR text, JSON grading data, .xlsx statistics files, and PDF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python packages and Tesseract OCR for image recognition and report generation.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
