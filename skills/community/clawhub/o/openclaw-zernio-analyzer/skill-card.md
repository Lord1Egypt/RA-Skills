## Description:

Analyzes Zernio.com profiles, posts, companies, jobs, and trends to extract structures, networks, engagement, and career insights from URLs and content requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and analyze public Zernio profile, post, company, job, and trend pages for structured summaries, network context, engagement signals, and career insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch and analyze profile or network information without making that retrieval clear to the user.

Mitigation: Disclose when public Zernio content is being retrieved and analyzed, especially for profile and network requests.

Risk: Weak URL scoping could cause the agent to fetch ambiguous or unintended Zernio-related URLs.

Mitigation: Validate requested URLs against public Zernio profile, post, company, and job patterns before retrieval.

Risk: Hidden activation for ambiguous requests could surprise users or analyze content outside their intent.

Mitigation: Ask for clarification when a request is ambiguous instead of silently activating the skill.

## Reference(s):

- [OpenClaw Zernio Analyzer on ClawHub](https://clawhub.ai/igorganapolsky/skills/openclaw-zernio-analyzer)
- [Publisher Profile](https://clawhub.ai/user/igorganapolsky)
- [Zernio Patterns Reference](artifact/references/zernio_patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or JSON-style structured analysis, with optional shell command examples for fetching public Zernio URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may summarize profile folders, network hierarchy, insights, engagement, and fetched public Zernio content.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
