## Description:

Search song lyrics by title and artist using the LrcApi public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hone1983](https://clawhub.ai/user/hone1983)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up lyrics for a requested song by title and, when available, artist, then present the result as readable text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Song title and artist queries are sent to the public api.lrc.cx lyrics API.

Mitigation: Avoid using the skill for private, sensitive, or unreleased song information when disclosure to the public API would be a concern.

Risk: The public lyrics API may be slow or fail to find a match.

Mitigation: Use a reasonable timeout and retry with only the song title or alternate spellings when no result is returned.

## Reference(s):

- [LrcApi lyrics endpoint](https://api.lrc.cx/lyrics?title={title}&artist={artist})

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown lyrics output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lyrics may include LRC timestamps and metadata that the skill directs the agent to remove for clean display.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
