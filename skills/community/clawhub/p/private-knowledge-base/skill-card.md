## Description:

Personal knowledge base for PDFs, papers, and documents with cross-document Q&A and concept retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirec-yzx](https://clawhub.ai/user/wirec-yzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to ingest local PDFs or folders, search stored document text, and summarize concepts across a personal document collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ingestion workflow can execute unsafe behavior when run on files or paths supplied by untrusted parties.

Mitigation: Ingest only trusted PDFs and folders, and review or harden the Python interpolation and JSON/search handling before using untrusted inputs.

Risk: The knowledge base retains private document text and source paths on disk.

Mitigation: Set KB_ROOT to a private location with restrictive permissions, avoid sensitive documents unless retention is acceptable, and delete stored text and metadata when no longer needed.

## Reference(s):

- [Knowledge Base Index Schema](references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and cited document names when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local knowledge-base text, metadata, and index files under KB_ROOT when ingestion scripts are run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
