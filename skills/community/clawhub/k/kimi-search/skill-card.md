## Description:

Kimi Search lets an agent use Moonshot Kimi's built-in web search tool to answer Chinese or English queries that need current web information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisbdz](https://clawhub.ai/user/chrisbdz)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to ask Moonshot Kimi for web-grounded answers when current information is needed. It requires a Moonshot API key and returns the original query, an answer, and token usage data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make repeated paid Moonshot API and web-search calls without a local request limit.

Mitigation: Use an isolated environment, protect and rotate MOONSHOT_API_KEY, monitor Moonshot usage, and add a local request or tool-call limit before regular use.

Risk: Search queries are sent to Moonshot for processing.

Mitigation: Avoid sending confidential or regulated content unless Moonshot processing is approved for the intended use case.

## Reference(s):

- [Moonshot Open Platform](https://platform.moonshot.cn)
- [Kimi Web Search Documentation](https://platform.moonshot.cn/docs/guide/use-web-search)
- [Moonshot Chat Pricing](https://platform.moonshot.cn/docs/pricing/chat)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON containing query, answer, and usage fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOONSHOT_API_KEY and may consume paid Moonshot API and web-search usage.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
