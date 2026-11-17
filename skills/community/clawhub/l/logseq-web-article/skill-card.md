## Description:

Fetch article content from general web page URLs, and call logseq-article-archive to organize, summarize, and archive the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesopodamia](https://clawhub.ai/user/mesopodamia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch web article content, convert it to Logseq-friendly Markdown, and pass it to a Logseq article archiving workflow for summarization and organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to automatically install logseq-article-archive without a pinned source or explicit user approval.

Mitigation: Review the dependency before use, require user approval before installation, and prefer a verified publisher or immutable release.

Risk: Fetched article content can include inaccessible, incomplete, or irrelevant page material.

Mitigation: Use clear article URLs and review the fetched Markdown and summary before relying on the archived result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mesopodamia/skills/logseq-web-article)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown article content with summary and article metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on logseq-article-archive for secondary analysis, summarization, and archiving.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
