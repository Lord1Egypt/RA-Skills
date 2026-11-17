## Description:

Find public sources or reuse searchable private documents across agent sessions. Evaluate search and initial base capacity before buying expansion or processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrpbr](https://clawhub.ai/user/wrpbr)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use OKF Index to find public source collections, search authorized private documents, and reuse evidence across sessions with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Importing private documents stores their contents in an OKF Index base and may involve storage or processing charges.

Mitigation: Approve the specific documents and destination base first, review retention, deletion, and costs, and use local files when external storage is unsuitable.

Risk: Indexed public-source metadata may be incomplete or out of date, especially for legislation.

Mitigation: Check the source, version, and coverage, and read the cited source text before relying on it.

## Reference(s):

- [OKF Index task index](https://okfindex.com/llms.txt)
- [OKF Index MCP endpoint](https://okfindex.com/mcp)
- [OKF Index bases API](https://okfindex.com/api/bases)
- [OKF Index pricing](https://okfindex.com/api/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with cited source passages and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-backed answers can include document links, hashes, and import dates when available.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
