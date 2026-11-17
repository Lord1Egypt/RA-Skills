## Description:

Read a Google results page. Use when the user says things like "what ranks on Google for best crm for startups", "show me the top 10 results for this keyword" or "who is in the local pack for plumber in Austin". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve localized Google search results for a keyword and summarize result positions, titles, domains, and snippets, with optional ads and other SERP features when a provider returns them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A search run is billed per call.

Mitigation: Inspect the endpoint and its list price, show the price to the user, and run only after the user approves.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/walidboulanouar/skills/looot-google-serp)
- [looot setup guide](https://looot.ai/skill.md)
- [Google SERP skill page](https://looot.ai/agent-skills/google-serp)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text or Markdown summary of structured Google search results, including positions, titles, links, and snippets; optional SERP features may be included.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are localized by country and language and represent a timestamped search snapshot; available SERP features vary by provider.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
