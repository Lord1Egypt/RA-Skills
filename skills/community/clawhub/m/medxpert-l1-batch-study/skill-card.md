## Description:

Batch-read a document or knowledge-base corpus with a local Qwen model through the DSH task bridge, producing structured Markdown summaries and a consolidated list of open questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Document and knowledge-base owners can use this skill to process a corpus in batches and receive one structured summary per document plus a consolidated list of unresolved questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Matching task summaries can overwrite one another.

Mitigation: Use a dedicated output folder and a trusted task-to-document mapping.

Risk: Private documents could be handled by an unintended local model or with unintended document permissions if the separately installed DSH bridge is misconfigured.

Mitigation: Before processing private material, verify the bridge's configured local model and document access permissions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/medxpert-l1-batch-study)
- [Publisher homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown files containing per-document summaries and a consolidated open-questions list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured summaries include key points, table highlights, and questions for follow-up.]

## Skill Version(s):

1.1.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
