## Description:

Fast, reliable Hong Kong bus ETA lookup for KMB, CTB, and LWB routes with fuzzy stop matching, bilingual output, multi-route parallel queries, and fixed no-result fallback handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomfong](https://clawhub.ai/user/tomfong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and compatible AI agents use this skill to answer Hong Kong public bus arrival-time questions in Traditional Chinese or English. It runs local Python scripts to query public KMB/LWB and Citybus data sources, match stops, and return concise ETA results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to Hong Kong public transit data APIs and maintains skill-local SQLite/JSON cache files.

Mitigation: Install only when those network requests and local cache files are acceptable for the deployment environment.

Risk: The cache sync can run in the background when local data is stale.

Mitigation: Review or disable background cache refresh behavior if every network update must be manually initiated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomfong/skills/hk-bus-eta)
- [KMB/LWB ETA data API](https://data.etabus.gov.hk/v1/transport/kmb/)
- [Citybus ETA data API](https://rt.data.gov.hk/v2/transport/citybus/)
- [DATA.GOV.HK public transport data](https://data.gov.hk/)
- [Artifact technical reference](artifact/README.md)
- [Artifact agent specification](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with route labels, stop links, grouped destinations, up to three upcoming ETAs, and fixed fallback messages when no ETA is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual zh-HK/en output; ETA freshness depends on public transit API responses and skill-local cache state.]

## Skill Version(s):

1.0.2 (source: server release metadata, README, changelog, and script headers)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
