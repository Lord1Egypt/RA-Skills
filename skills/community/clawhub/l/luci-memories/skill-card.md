## Description:

Search personal video memory, including videos, images, keyframes, transcripts, traits, events, relationships, and speeches, when a user asks about their media, what happened, what was said, who they know, or their personality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memories-ai-official](https://clawhub.ai/user/memories-ai-official)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search a user's personal media memory and portrait data, then answer questions about videos, images, recordings, people, events, relationships, and speech using retrieved results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses personal media, transcripts, portrait traits, events, relationships, and speeches through Memories.ai services.

Mitigation: Install only when the user trusts Memories.ai with this personal data and understands that retrieved results may contain sensitive memories or identities.

Risk: The security evidence reports that MEMORIES_AI_KEY may be stored in a plaintext local .env file.

Mitigation: Prefer a protected secret mechanism for MEMORIES_AI_KEY, restrict local file permissions if a .env file is used, and avoid committing or sharing the key.

Risk: The security evidence reports sensitive media exposure through non-expiring unauthenticated image references.

Mitigation: Avoid sharing logs, transcripts, bucket values, or blob values until media URLs are authenticated, expiring, and revocable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/memories-ai-official/skills/luci-memories)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted search results and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include media, transcript, event, trait, relationship, speech, timestamp, location, bucket, and blob fields returned by the Luci-memory APIs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
