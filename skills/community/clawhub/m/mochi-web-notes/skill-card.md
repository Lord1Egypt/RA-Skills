## Description:

Turn one to three explicitly supplied public HTTPS pages into source-backed Chinese or English research notes saved locally. Use for Web Research Notes, comparing a few linked articles, or a first cited reading note; not crawling, paywalls, logged-in pages or sending reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read up to three public web pages they provide and create cited Chinese or English research notes with source links, page dates, and excerpts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected websites receive requests, and collected page text may be sent to the user's configured model provider.

Mitigation: Supply only public links without credentials or session tokens, and follow the configured provider's data terms.

Risk: Generated notes may contain claims that are not fully supported by the collected page text.

Mitigation: Review each claim and citation against the linked source pages.

## Reference(s):

- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-web-notes)
- [MochiLab homepage](https://mochilab.bz)
- [MochiLab setup guide](https://mochilab.bz/Skills/Connect.aspx?lang=en)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Research guidance]

**Output Format:** [Cited Markdown research notes and JSON source evidence records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local workspace files; one to three explicitly supplied public HTTPS sources; English or Simplified Chinese]

## Skill Version(s):

1.0.1 (source: server-resolved release and metadata.openclaw)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
