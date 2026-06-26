## Description: <br>
Medical Record Translator produces structure-preserving, Chinese-first translations of medical records, lab reports, discharge summaries, prescriptions, pathology and radiology reports, and similar documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helenalhq](https://clawhub.ai/user/helenalhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and medical-document reviewers use this skill to translate medical records into doctor-readable Markdown while preserving source structure, anchors, tables, key-value fields, original text, and low-confidence markings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical records may contain sensitive personal health information that is sent to the configured AI provider during translation. <br>
Mitigation: De-identify patient information when possible and use an approved local or enterprise model for regulated or sensitive data. <br>
Risk: Rendered PDF export depends on pinned third-party PDF and Markdown packages. <br>
Mitigation: Review the pinned rendering dependencies before installing them and run the included PDF check after export. <br>
Risk: Medical translation errors or low-confidence OCR regions can affect clinical meaning. <br>
Mitigation: Preserve original text and anchors, mark uncertainty at the smallest useful scope, and review clinically important low-confidence items against the source document. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helenalhq/medical-record-translator) <br>
- [Output Contract](references/output-contract.md) <br>
- [Block Model](references/block-model.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [Medical Terminology Reference](references/terminology.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese-first, original-preserving Markdown with optional PDF export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves page/block anchors, source block order, tables, key-value regions, original text, and low-confidence review markers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
