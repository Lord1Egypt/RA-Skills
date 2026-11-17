## Description:

Automatically detect and de-identify PII and PHI from clinical or medical text for HIPAA-oriented review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare, compliance, and data engineering teams use this skill to scan clinical text for HIPAA Safe Harbor identifier categories and produce de-identified text with reviewable detection details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes medical text and may miss context-dependent identifiers or other PHI.

Mitigation: Require manual HIPAA review of de-identified output before any release or downstream use.

Risk: Audit logs and console output can retain sensitive context or patient details from detections.

Mitigation: Use secured storage for audit logs, limit console exposure, and avoid running on real PHI unless logs are protected or redacted.

Risk: The validation status can report APPROVED even though it is not compliance proof.

Mitigation: Treat automated status as a triage signal only and document reviewer decisions for compliance workflows.

Risk: Unpinned or optional NLP dependencies can change detection behavior across environments.

Mitigation: Pin dependencies and spaCy models in an isolated environment before processing sensitive records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/hipaa-compliance-auditor)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)
- [HIPAA Safe Harbor guide](references/hipaa_safe_harbor_guide.md)
- [PII pattern reference](references/pii_patterns.json)
- [Dependency reference](references/requirements.txt)
- [HHS guidance on de-identification](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Plain text and JSON audit logs, with Markdown guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces semantic replacement tokens, detection metadata, confidence scores, and validation status for human review.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
