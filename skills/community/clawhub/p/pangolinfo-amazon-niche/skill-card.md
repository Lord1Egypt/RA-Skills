## Description:

Helps agents browse and search Amazon category trees, resolve category paths, filter category metrics, and identify low-competition niche opportunities using Pangolinfo MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangolinfo](https://clawhub.ai/user/pangolinfo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to research Amazon categories and niches, including category browsing, category path resolution, metric-based category filtering, and niche screening for product research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure risk from Pangolinfo API keys appearing in URLs, logs, shell history, or shared transcripts.

Mitigation: Keep keys in the MCP server or a secret manager, avoid putting JWTs in URLs or chat messages, and rotate any key that may have been exposed.

Risk: Incorrect Amazon research conclusions if an agent fabricates unavailable metrics or treats raw tool output as user-facing analysis.

Mitigation: Use only returned MCP data, identify missing fields plainly, and summarize results as structured category or niche findings instead of raw JSON.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pangolinfo/skills/pangolinfo-amazon-niche)
- [Pangolinfo website](https://www.pangolinfo.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown summaries with structured category, metric, and niche findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid raw JSON and present sourced category or niche metrics in the user's language.]

## Skill Version(s):

4.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
