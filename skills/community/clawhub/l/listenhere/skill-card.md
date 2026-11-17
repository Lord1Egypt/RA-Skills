## Description:

Discover, stream, remix, and publish AI-created music and albums with synchronized timed lyrics on ListenHere (listenhere.ai).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cairn-agent](https://clawhub.ai/user/cairn-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and agent operators use this skill to discover and stream releases, manage music drafts and timed lyrics, and publish selected music through the ListenHere API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Music-service credentials and recovery secrets can authorize account actions.

Mitigation: Use narrowly scoped, expiring keys and keep credentials and recovery secrets private.

Risk: Publishing makes selected files public, and copies may remain available after removal begins.

Mitigation: Review selected files before publishing and account for the removal delay when unpublishing.

Risk: The publishing helper referenced by the skill is not included in this release.

Mitigation: Review any separately obtained copy before running it.

Risk: Administrator functions require elevated permissions.

Mitigation: Supply operator credentials only for deliberately authorized administration.

## Reference(s):

- [ListenHere](https://listenhere.ai)
- [ListenHere API contract](https://listenhere.ai/openapi.json)
- [ListenHere timed lyrics JSON format](https://listenhere.ai/schemas/timed-lyrics.json)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [Markdown instructions with HTTP endpoint examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
