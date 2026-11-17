## Description:

Multi-source search skill for Kiro on OpenClaw. Aggregate and rank results from Google, Google Scholar, YouTube, and X, then output a concise brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vmining](https://clawhub.ai/user/vmining)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to gather search results across web, scholarly, video, and X sources, then receive a ranked brief with top results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A SerpAPI error can expose the API key in saved output or logs.

Mitigation: Avoid enabling the Scholar source with a real SerpAPI key until error handling redacts api_key values from exceptions, stdout, latest.json, and latest.md.

Risk: Search queries are sent to external providers.

Mitigation: Use only non-sensitive search queries and review provider access requirements before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vmining/skills/kiro-search-aggregator)
- [OpenClaw](https://openclaw.ai)
- [Serper API endpoint](https://google.serper.dev)
- [SerpAPI search endpoint](https://serpapi.com/search.json)
- [X recent search endpoint](https://api.x.com/2/tweets/search/recent)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Console JSON plus latest.json and latest.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes results to outputs/search-aggregator by default.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
