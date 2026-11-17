## Description:

Search and analyze the Jeffrey Epstein email archive, iMessages, documents, photos, and people through jmail.world's Data API, DuckDB/Parquet datasets, web search API, and file downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabudde](https://clawhub.ai/user/fabudde)

### License/Terms of Use:

MIT

## Use Case:

External researchers and developers use this skill to search public Epstein archive emails, iMessages, documents, photos, and identified people through jmail.world APIs and local DuckDB/Parquet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled shell scripts contact external services, cache public datasets locally, and save downloaded files.

Mitigation: Review before installing, avoid elevated privileges, use a private working directory, and treat downloaded PDFs, images, and cached Parquet files as untrusted content.

Risk: Security evidence reports under-disclosed local file writes and unsafe cache/query handling risks.

Mitigation: Inspect script behavior before use, avoid sensitive output directories, and verify query and download inputs before executing commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fabudde/skills/jmail)
- [Jmail Homepage](https://jmail.world)
- [Official Docs](https://jmail.world/docs/introduction)
- [Docs Index for LLMs](https://jmail.world/docs/llms.txt)
- [API Reference](references/api-docs.md)
- [DuckDB Examples](https://jmail.world/docs/duckdb)
- [Datasets & URLs](https://jmail.world/docs/datasets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API URLs, DuckDB SQL examples, and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to run bundled shell scripts that contact jmail.world, data.jmail.world, and assets.getkino.com, cache public Parquet datasets locally, and save downloaded documents or images.]

## Skill Version(s):

1.6.5 (source: server release metadata; artifact frontmatter says 1.6.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
