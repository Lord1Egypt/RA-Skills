## Description:

Provides structured-knowledge and factual lookup workflows through Pilot Protocol service agents for Knowledge Graph, DuckDuckGo Instant Answers, Archive.org, holidays, geocoding, Wikipedia, Wikiquote, and university data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agents use this skill to discover and query Pilot Protocol knowledge service agents for entity lookup, public-holiday calendars, archive search, geocoding, and related factual data retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may expose sensitive private data to Pilot Protocol service agents or external upstream data sources.

Mitigation: Avoid sending secrets, personal data, or private business data in filters, free-text queries, or Gemini summary requests.

Risk: Lookup results and Gemini-generated summaries can be incomplete, stale, or misleading because they are best-effort outputs from upstream sources.

Mitigation: Verify important results against authoritative sources and prefer structured /data responses with upstream URLs when accuracy matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-knowledge)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses are retrieved through pilotctl inbox after an ACK envelope; structured data responses can include items, counts, pagination fields, truncation status, and upstream URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
