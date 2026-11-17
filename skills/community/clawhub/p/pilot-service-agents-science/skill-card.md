## Description:

Primary-source scientific and research APIs for earthquakes, molecules, space weather, particle physics, volcanoes, and related open-data catalogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and external users use this skill to discover and query Pilot Protocol science service agents for structured research data, natural-event streams, chemistry records, space data, and open-data catalog metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and free-text requests are sent to remote service agents and may reveal sensitive research interests or terms.

Mitigation: Avoid sending confidential, personal, regulated, or proprietary data in filters or free-text prompts.

Risk: The service catalog is broader than the short description and may not be the right path for scholarly literature searches.

Mitigation: Use the dedicated academic skill for literature, citations, and scholarly paper discovery.

Risk: Agent availability and filter contracts can change as the Pilot Protocol catalog evolves.

Mitigation: Run a fresh list-agents query and read the target agent's /help response before relying on a query shape.

Risk: Natural-language summaries and free-text responses may be incomplete or inaccurate.

Mitigation: Prefer structured /data responses and inspect upstream URLs or source metadata when accuracy matters.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-science)
- [Publisher Profile](https://clawhub.ai/user/teoslayer)
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include ACK envelopes followed by JSON inbox entries; summaries and free-text requests may return prose.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
