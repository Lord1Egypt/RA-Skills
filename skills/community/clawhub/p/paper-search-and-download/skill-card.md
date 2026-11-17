## Description:

Searches arXiv for papers by topic and date range or from a seed paper title or arXiv ID, then downloads matching PDFs with structured filenames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppingzhang](https://clawhub.ai/user/ppingzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to collect arXiv papers for a topic or related to a seed paper, with optional publication date and result-count constraints. It helps agents retrieve PDFs into a local output directory and report how many papers were found, downloaded, or skipped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can fall back to unverified HTTPS if local certificate validation fails, which may allow tampered PDFs to be saved.

Mitigation: Review the skill before use, remove the insecure TLS fallback or run only on trusted networks, and confirm the local certificate store is working.

Risk: Search terms are sent to arXiv and retrieved PDFs are written to the selected output directory.

Mitigation: Avoid sensitive search queries and choose an output directory appropriate for downloaded research files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ppingzhang/skills/paper-search-and-download)
- [arXiv API Query Endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands and downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads PDFs to a configurable output directory, defaulting to ./arxiv, and names files with arXiv version and update date.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
