## Description:

Space and astronomy skill for querying NASA Astronomy Picture of the Day metadata and media URLs and Open Notify astronaut status through Pilot Protocol service agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and external agents use this skill to discover space-data service agents, inspect their filter contracts, and request structured data or concise summaries for APOD and current-astronaut queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filters, free-text prompts, and summary requests are sent through the Pilot Protocol network.

Mitigation: Avoid including private, regulated, or confidential data in queries or prompts.

Risk: Summary and free-text responses may contain Gemini-generated prose.

Mitigation: Treat generated prose as advisory and verify important facts against the structured data or upstream source.

Risk: The skill depends on pilotctl, a running daemon, network 9 membership, and reachable service agents.

Mitigation: Confirm the Pilot Protocol environment and agent contracts with fresh list-agents and /help queries before relying on results.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-space)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include structured JSON envelopes or Gemini-generated prose summaries returned through Pilot Protocol inbox messages.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
