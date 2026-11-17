## Description:

Normalizes papers, PDFs, URLs, and literature notes into structured research records for project memory and retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and research operations teams use this skill to turn papers, PDFs, URLs, raw text, or metadata into normalized literature records for project memory and retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prepare records intended for shared or persistent project memory.

Mitigation: Review the writeback payload before saving it, and require a project_id before any writeback.

Risk: Incomplete or ambiguous paper metadata can lead to misleading normalized records.

Mitigation: Use null values for missing fields, populate uncertain_fields, and separate direct observations from claimed interpretations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunbinnju-star/skills/paper-ingest-normalizer)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Structured JSON-like research record with nullable fields and a writeback payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes uncertainty fields and a writeback readiness flag; no project memory writeback should occur without project_id.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
