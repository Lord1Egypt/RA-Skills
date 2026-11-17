## Description:

Games, manga/anime, trivia, and fandom APIs for Pilot Protocol service agents, including PokeAPI, Jikan, CheapShark, TVMaze, Shikimori, and Gutenberg data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agent users use this skill to discover and query entertainment-related Pilot Protocol service agents for Pokemon, anime and manga, TV, books, trivia, and game store metadata through pilotctl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and responses go through the Pilot Protocol overlay rather than staying local.

Mitigation: Install and use this skill only when Pilot Protocol service-agent queries are intended, and avoid sending sensitive data unless the overlay controls meet the deployment's requirements.

Risk: Natural-language summaries and free-text responses are generated text and may be incomplete or inaccurate.

Mitigation: Prefer structured /data queries for factual lookups and verify generated summaries against returned items or upstream sources.

Risk: The listed entertainment agents are a snapshot and the catalogue can change.

Mitigation: Run a fresh list-agents query and read each selected agent's /help contract before relying on filters or availability.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-entertainment)
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON query and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, the pilot-protocol and pilot-service-agents skills, a running Pilot Protocol daemon joined to network 9, and access to the list-agents directory agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
