## Description:

This skill helps Chinese primary and middle school teachers grade photographed or scanned homework, map results to curriculum knowledge points, generate student and class mastery assessments, and produce role-aware learning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, school administrators, and education technology teams use this skill to design workflows for OCR-assisted homework grading, knowledge-point mastery analysis, student and class reports, and permission-scoped access to academic data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Student homework, names, class information, and academic performance data may be exposed if the OCR service or storage layer is deployed without sufficient protection.

Mitigation: Bind local OCR services to localhost or place them behind authenticated TLS, enforce role-based access controls, add upload and rate limits, and define consent, retention, deletion, and audit rules before processing student data.

Risk: Unpinned OCR containers or dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin and verify OCR container images and model artifacts before deployment, and review updates before using them in a school environment.

Risk: OCR and AI grading may misread handwriting or produce incorrect scoring and learning advice.

Mitigation: Keep teacher review in the grading workflow, especially for subjective answers, low-confidence OCR results, and student-facing feedback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-homework-grading)
- [Data Model Reference](references/data-model.md)
- [Permission Model Reference](references/permission-model.md)
- [Assessment Chart Specification](references/chart-spec.md)
- [OCR Implementation Plan](references/ocr-implementation.md)
- [OCR Selection Guidance](references/ocr-selection.md)
- [Textbook Mapping Plan](references/textbook-mapping.md)
- [Textbook Version Mapping Plan](references/textbook-version-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, TypeScript, SQL, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes education data models, OCR deployment examples, chart specifications, permission rules, and textbook mapping guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
