## Description:

Batch process and index OneDrive photos by name, date, size, format, and album; run OCR or multimodal recognition; support full indexing, hash-based incremental skipping, semantic search, move, upload, delete, restore, and recycle-bin governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanqeur](https://clawhub.ai/user/lanqeur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search, OCR, index, semantically retrieve, organize, export, and recover OneDrive photo collections. It is useful when an agent needs guided shell commands and configuration for batch photo workflows against Microsoft OneDrive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk indexing can disclose private photos, extracted OCR text, embeddings, and semantic-search queries to the configured OCR or embedding provider.

Mitigation: Review the configured provider and endpoint, use trusted HTTPS endpoints, limit batches and filters to intended photos, and treat extracted text and queries as sensitive data.

Risk: The skill persists Microsoft authentication tokens and uses API keys for OCR and embedding services.

Mitigation: Protect the config file and token cache, avoid sharing the workspace, grant only the scopes required for the intended workflow, and rotate credentials if they may have been exposed.

Risk: Write-capable workflows can delete, move, restore, upload, or empty recovery copies, and local recovery copies older than 15 days may be removed automatically.

Mitigation: Keep the default read-only mode and Files.Read scope unless write actions are intentional, test with small limits before bulk changes, avoid hard delete unless required, and restore needed files within the retention window.

## Reference(s):

- [Config Example](references/config.example.json)
- [ClawHub Skill Page](https://clawhub.ai/lanqeur/skills/onedrive-photo-batch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime commands emit JSON and can export JSON or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configuration guidance for Microsoft authentication, OCR and embedding providers, concurrency, download rate limits, read-only mode, and recycle-bin behavior.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
