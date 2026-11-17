## Description:

Knowledge Base converts documents to Markdown, classifies and indexes them locally, and supports keyword and semantic search for a private knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to ingest local documents into a private knowledge base, organize them by category, and retrieve relevant content through keyword or vector search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom category names can cause imported documents to be written outside the intended knowledge-base folder.

Mitigation: Validate or patch category input before using custom categories, and restrict categories to known local folder names.

Risk: Setup and vector search features install unpinned packages into the active Python environment.

Mitigation: Install and run the skill only inside a dedicated virtual environment with reviewed dependency versions.

Risk: Watch mode, cron import, and broad batch scans can store and index unintended local files.

Mitigation: Use dry-run or one-time scans first, and point automated import only at directories containing files intended for the knowledge base.

Risk: Deleting a document removes stored knowledge-base content.

Mitigation: Back up the knowledge-base directory or confirm document IDs before using delete operations.

## Reference(s):

- [ClawHub Knowledge Base release](https://clawhub.ai/michealxie001/skills/knowledge-base-001)
- [Microsoft MarkItDown documentation](https://github.com/microsoft/markitdown)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, JSON CLI responses, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores converted content and indexes under the local knowledge-base directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
