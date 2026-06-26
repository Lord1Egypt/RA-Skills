## Description: <br>
Extract data from construction images using AI Vision. Analyze site photos, scanned documents, drawings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction teams, developers, and project analysts use this skill to extract structured text, tables, detected objects, progress estimates, and safety observations from construction photos, scanned documents, sketches, and drawings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Construction photos, scans, drawings, and extracted text may contain sensitive site, client, personnel, or project details, and the skill may use configured external vision providers. <br>
Mitigation: Use only with organization-approved AI providers, scoped provider API keys, and redaction of sensitive details where possible. <br>
Risk: Vision, OCR, progress, and safety observations can be uncertain when images are low quality, ambiguous, or incomplete. <br>
Mitigation: Review outputs before using them for project, compliance, or safety decisions, and preserve confidence scores and warnings in downstream reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/image-to-data) <br>
- [Publisher profile](https://clawhub.ai/user/datadrivenconstruction) <br>
- [Data-Driven Construction](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured Markdown, tables, or JSON with confidence scores and warnings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include extracted text, detected objects, table records, progress estimates, annotated descriptions, and low-confidence warnings.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
