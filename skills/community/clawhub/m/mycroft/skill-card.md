## Description:

EPUB and ebook ingestion, local vector index, and Q&A CLI for books.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabe](https://clawhub.ai/user/fabe)

### License/Terms of Use:


## Use Case:

Developers and readers use this skill to configure and operate the mycroft CLI for ingesting EPUBs and ebooks, building a local vector index, searching passages, and asking questions about book content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external npm CLI that executes with access to user-provided credentials and local book data.

Mitigation: Review the npm package source and install a pinned, audited version before use.

Risk: Commands that use OPENAI_API_KEY may process book content through external API calls.

Mitigation: Provide only API keys and ebook paths that are appropriate for this workflow and data handling context.

Risk: The delete command can bypass confirmation when run with --force.

Mitigation: Avoid --force in scripted runs unless the target book ID and deletion behavior have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fabe/skills/mycroft)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the mycroft CLI is installed and OPENAI_API_KEY is available when embeddings, Q&A, search, or chat commands require it.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
