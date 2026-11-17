## Description:

Provides music metadata and lyrics lookup workflows for iTunes search and Lyrics.ovh through Pilot Protocol service agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

External developers and agent users use this skill to discover music service agents, search iTunes metadata, fetch lyrics, and request summaries through Pilot Protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form queries and summary requests may send private or sensitive text through Pilot Protocol service agents and external services, including Gemini summaries.

Mitigation: Avoid private or sensitive text in music queries, lyric requests, and summary prompts; review outgoing requests before sending them.

Risk: Lyrics and metadata are best-effort lookups, and the artifact does not guarantee lyric licensing rights.

Mitigation: Verify licensing and usage rights separately before reusing lyrics or metadata in commercial materials.

Risk: The skill depends on pilotctl, a running Pilot Protocol daemon, network 9 membership, and reachable service agents.

Mitigation: Confirm dependencies and run fresh list-agents and /help queries before relying on a specific agent contract.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-music)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The service agents return ACK envelopes first; actual lookup results are read from the pilotctl inbox as JSON data or prose summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
