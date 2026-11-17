## Description:

Search and download related arXiv papers by topic plus date range, or from a seed paper title/id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppingzhang](https://clawhub.ai/user/ppingzhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect arXiv papers for a topic, date range, or seed paper and save downloaded PDFs with deterministic filenames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader performs outbound web requests and writes files locally.

Mitigation: Use a confined output directory, keep max-results small, and review the destination before running.

Risk: The security scan says the downloader can fetch unverified links and lacks resource limits.

Mitigation: Prefer a revised version that allowlists arXiv PDF hosts, validates redirects and PDF content, and enforces file-size and batch-size limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppingzhang/skills/paper-search-and-download-automatically)
- [Publisher profile](https://clawhub.ai/user/ppingzhang)
- [arXiv API endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and locally downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an output directory and names PDF files using arXiv version/date plus sanitized title.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
