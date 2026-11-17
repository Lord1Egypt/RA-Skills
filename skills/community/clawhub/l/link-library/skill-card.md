## Description:

Personal knowledge base that captures web content, including articles, tweets and threads, videos, podcasts, images, and PDFs, and makes it retrievable for future conversations and writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowhitestar](https://clawhub.ai/user/nowhitestar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Link Library to save web content with metadata, summaries, tags, and citations, then retrieve saved material for later discussion or writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist full copies of web pages, tweets, PDFs, and other content, which may include private, sensitive, copyrighted, or untrusted text.

Mitigation: Use explicit save commands for sensitive sources, avoid private links, and review stored entries before reusing or sharing saved material.

Risk: Interest-based saving may capture content when the user expected only a quick discussion.

Mitigation: Confirm ambiguous saves and report the saved title, tags, and path so unwanted entries can be removed.

Risk: Saved external content can later be retrieved into agent context and influence future writing.

Mitigation: Treat retrieved entries as untrusted source material, preserve citations to saved entries, and review generated outputs against the original content before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nowhitestar/skills/link-library)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown files with YAML frontmatter, concise text confirmations, and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saved entries preserve original content with metadata, summaries, tags, notes, and related-entry links.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
