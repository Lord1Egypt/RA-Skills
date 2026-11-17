## Description:

Search the web using multiple engines (Tavily, multi-search-engine, or SearXNG).

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollisken](https://clawhub.ai/user/hollisken)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve web search results through Tavily, SearXNG, or multi-engine search for news, technical materials, papers, and general web queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send search queries to third-party services.

Mitigation: Review expected query sensitivity before installation and configure approved search providers for the deployment environment.

Risk: The security summary reports a shared hardcoded Tavily fallback credential.

Mitigation: Prefer a version that removes the embedded key and require deployment-specific credentials through TAVILY_API_KEY.

Risk: The security guidance reports possible execution of an external Python script from a fixed Windows path that is not included in the reviewed package.

Mitigation: Prefer reviewed in-package provider code or document and review all subprocess behavior before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hollisken/skills/kn70-search)
- [Publisher Profile](https://clawhub.ai/user/hollisken)
- [Tavily Search API Endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, JSON, links, guidance]

**Output Format:** [JSON object containing success status, selected engine, message, and search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count is controlled by max_results; the plugin declares a 20 calls/minute rate limit.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill.yaml, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
