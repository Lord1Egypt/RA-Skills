## Description:

Extract data from construction images using AI Vision. Analyze site photos, scanned documents, drawings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers and construction teams use this skill to extract structured data, OCR text, tables, object detections, progress estimates, and safety observations from construction photos, scanned documents, sketches, and drawings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample analysis routines may produce fabricated progress, safety, or construction findings without real image inspection.

Mitigation: Replace simulated routines with validated OCR, object-detection, and vision backends before relying on outputs, and clearly label result provenance and uncertainty.

Risk: Construction safety, compliance, progress, and reporting outputs may be inaccurate or incomplete.

Mitigation: Use outputs as review aids only and require qualified human validation before operational, safety, compliance, or reporting decisions.

Risk: Images may contain sensitive project, personnel, site, or drawing details that are sent to external vision APIs.

Mitigation: Redact sensitive details where possible and confirm that API use, retention, and access controls match project confidentiality requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/skills/image-to-data)
- [Data-Driven Construction Website](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, JSON, and tabular structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence scores, annotated findings, warnings for low-quality or ambiguous image regions, and behavior constrained by the selected vision API provider.]

## Skill Version(s):

2.0.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
