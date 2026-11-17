## Description:

Search Kagi's unique non-commercial web (Teclis) and non-mainstream news (TinyGem) indexes for independent, ad-free content you won't find in regular search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelazar](https://clawhub.ai/user/joelazar)

### License/Terms of Use:


## Use Case:

Developers and researchers use this skill to query Kagi enrichment indexes for independent web sources, niche discussions, and non-mainstream news related to a topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper may download and execute a pre-built native binary when a local build is unavailable.

Mitigation: Prefer building from the included Go source, or manually verify a pinned release and checksum before running any downloaded binary.

Risk: Search queries are sent to Kagi and require a paid API key.

Mitigation: Use only with queries and environments appropriate for Kagi API processing, and configure KAGI_API_KEY through the user's shell environment.

## Reference(s):

- [Kagi Enrichment API documentation](https://help.kagi.com/kagi/api/enrich.html)
- [Kagi Enrich ClawHub page](https://clawhub.ai/joelazar/skills/kagi-enrich)
- [Publisher profile](https://clawhub.ai/user/joelazar)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text search results or structured JSON, with Markdown setup and usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KAGI_API_KEY and a Kagi account with API billing enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
