## Description:

Interviews a user and builds a personalized health-record workspace for organizing reports, ingesting PDFs, screenshots, and scans, tracking health data over time, and maintaining raw files, readable notes, structured data, and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsongra11](https://clawhub.ai/user/hsongra11)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and their assisting agents use this skill to organize sensitive health reports into a durable local workspace with preserved raw records, readable extractions, structured tracking data, and dashboard or history summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health records may be copied into a persistent local folder with raw files, extracted notes, structured data, and summaries.

Mitigation: Choose the storage location deliberately, confirm retention expectations, and limit access to the local workspace.

Risk: External OCR or API processing may disclose health files or extracted health data to a third-party provider.

Mitigation: Keep processing local by default and use external services only after explicit user approval for that workflow.

Risk: Extracted report content or summaries could be mistaken for medical advice.

Mitigation: Label outputs as organization and extraction aids, keep summaries traceable to source files, and avoid presenting findings as medical advice.

## Reference(s):

- [Workflow Reference](references/workflow.md)
- [Examples Reference](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/hsongra11/skills/health-records-ingest)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown notes, CSV/JSON tracking files, folder layouts, and summary documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves raw files; defaults to local-only processing and requires explicit consent before external OCR or API uploads.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
