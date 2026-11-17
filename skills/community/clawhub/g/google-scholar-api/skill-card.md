## Description:

Google Scholar API helps agents search Google Scholar through SerpAPI, extract academic paper metadata and citation details, and optionally download available PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rutianze](https://clawhub.ai/user/rutianze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research assistants use this skill to perform targeted literature searches, collect paper metadata such as authors, year, citations, and snippets, and optionally save available PDFs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SerpAPI keys may be exposed through plaintext configuration, logs, or backup commands.

Mitigation: Use a disposable or tightly scoped SerpAPI key, provide it through environment variables or a secret manager, and avoid printing, committing, or backing up the key in plaintext.

Risk: PDF download behavior can retrieve files from external sources with weak safeguards.

Mitigation: Prefer search-only mode by default, download only after reviewing the PDF source, and write files to a dedicated output directory.

Risk: Dependencies are version-ranged rather than pinned for reproducible shared or production use.

Mitigation: Pin and review dependencies before deploying the skill in shared, commercial, or production environments.

Risk: Academic content access and bulk downloading may implicate publisher terms, copyright, or rate limits.

Mitigation: Use modest request volumes, respect access terms and copyright, and avoid large-scale PDF downloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rutianze/skills/google-scholar-api)
- [API Guide](references/api_guide.md)
- [Usage Examples](references/usage_examples.md)
- [SerpAPI Search API](https://serpapi.com/search-api)
- [SerpAPI Google Scholar API](https://serpapi.com/google-scholar-api)
- [Google Scholar Help](https://scholar.google.com/intl/en/scholar/help.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown reports with optional JSON result files, Python snippets, shell commands, and downloaded PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local PDF downloads and search_results.json in the configured output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
