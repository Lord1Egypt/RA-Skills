## Description:

Markdown Fetcher helps an agent fetch public webpage content and convert it into readable Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaqi-guo-0114](https://clawhub.ai/user/jiaqi-guo-0114)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users can use this skill to retrieve public web articles or pages as Markdown for reading, summarization, extraction, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or private URLs could expose confidential content or tokens to third-party webpage conversion services.

Mitigation: Use the skill only for public webpages, and avoid private documents, authenticated pages, internal hosts, signed links, or URLs containing tokens or secrets.

Risk: The optional Scrapling fallback may introduce dependency risk if installed directly and without review.

Mitigation: Install Scrapling only when needed, use a disposable virtual environment or container, and prefer a pinned, reviewed version.

## Reference(s):

- [Markdown Fetcher ClawHub Page](https://clawhub.ai/jiaqi-guo-0114/skills/markdown-fetcher)
- [Scrapling GitHub Repository](https://github.com/D4Vinci/Scrapling)
- [markdown.new](https://markdown.new/)
- [defuddle.md](https://defuddle.md/)
- [Jina AI Reader](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown with URL patterns and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill prioritizes hosted webpage-to-Markdown services and suggests Scrapling only as a fallback.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
