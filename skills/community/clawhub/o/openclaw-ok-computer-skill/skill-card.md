## Description:

Runs concurrent DuckDuckGo searches for multiple topics and returns a structured JSON report of top results for broad research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grahammiranda13](https://clawhub.ai/user/grahammiranda13)

### License/Terms of Use:

MIT License

## Use Case:

External users, developers, and agent operators use this skill to collect high-level search results across several topics in parallel before deeper research or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to DuckDuckGo, which may expose sensitive or private research topics to an external service.

Mitigation: Do not submit confidential, regulated, or private queries unless the deployment has approved that data flow.

Risk: The dependency declaration uses an unpinned requests range and does not include a lock file or hashes.

Mitigation: Install in an isolated Python environment and pin direct and transitive dependencies before production deployment.

Risk: The skill depends on outbound network access and DuckDuckGo API availability.

Mitigation: Declare the outbound network requirement and handle empty, delayed, or failed search responses in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grahammiranda13/skills/openclaw-ok-computer-skill)
- [Publisher homepage](https://www.grahammiranda.com/)
- [DuckDuckGo Instant Answer API endpoint](https://api.duckduckgo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON search results with query, title, URL, and optional error fields; surrounding agent responses may be Markdown or shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses repeated query inputs and an optional max-results setting; results depend on DuckDuckGo availability and coverage.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
