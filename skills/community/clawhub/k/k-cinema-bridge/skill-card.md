## Description:

Query Korean multiplex (Lotte Cinema, CGV, Megabox) box office rankings and upcoming movie data enriched with KOBIS details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uyeong](https://clawhub.ai/user/uyeong)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer Korean cinema questions by fetching public box office and upcoming release data, then summarizing rankings, recommendations, age ratings, and movie details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Movie availability and rankings come from an external public API refreshed daily and may not reflect live ticketing inventory.

Mitigation: Present results as informational movie discovery data and avoid treating them as authoritative booking or availability guarantees.

Risk: Enriched KOBIS movie details may be null for some records.

Mitigation: Null-check detail fields and avoid guessing missing genres, credits, or release metadata.

## Reference(s):

- [K Cinema Bridge ClawHub listing](https://clawhub.ai/uyeong/skills/k-cinema-bridge)
- [K Cinema Bridge API](https://uyeong.github.io/k-cinema-bridge/)
- [OpenAPI specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Natural-language responses and Markdown tables based on JSON API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses unauthenticated public movie data refreshed daily; KOBIS detail records may be null.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
