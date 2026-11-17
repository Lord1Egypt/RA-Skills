## Description:

Extract main content text from an HTML page (URL, file, or stdin), stripping navigation, footers, ads, and boilerplate for downstream text analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktoetotam](https://clawhub.ai/user/ktoetotam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to extract readable article-style text from URLs, HTML files, or stdin before readability checks, sentiment analysis, summarization, embeddings, or corpus preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install unpinned Python packages into the active environment.

Mitigation: Install and run it only in an isolated environment, and prefer a release that declares and pins dependencies ahead of time.

Risk: The skill can fetch unrestricted URLs from the host network.

Mitigation: Avoid running it on sensitive networks or with privileged accounts; restrict or review remote URL fetching before use in controlled environments.

Risk: Extracted page text is untrusted input when passed to downstream tools or LLM workflows.

Mitigation: Review downstream handling of extracted content and avoid treating page text as trusted instructions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text by default, with optional Markdown or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status and errors are written to stderr so stdout remains suitable for piping.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
