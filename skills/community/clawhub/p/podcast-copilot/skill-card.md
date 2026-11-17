## Description:

Guides agents through Podwise CLI workflows for podcast discovery, transcript-grounded answers, media processing, and retrieval of transcripts, summaries, chapters, Q&A, mind maps, highlights, and keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skoowoo](https://clawhub.ai/user/skoowoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to choose Podwise CLI workflows for podcast discovery, transcript-grounded question answering, episode processing, and retrieval of summaries, transcripts, chapters, highlights, mind maps, Q&A, and keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill depends on the Podwise CLI and a configured API key.

Mitigation: Check Podwise CLI availability and configuration before running workflows, and stop with setup guidance if either prerequisite is missing.

Risk: Processing URLs or local audio and video can upload content to Podwise and consume quota or credits.

Mitigation: Require explicit user confirmation before process commands unless the user already asked to proceed, and disclose quota and upload behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and scannable result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Podwise episode URLs, processing status, transcript-derived answers, source excerpts when requested, and unavailable-artifact notes.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
