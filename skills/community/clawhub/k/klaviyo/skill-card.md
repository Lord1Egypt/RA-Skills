## Description: <br>
Klaviyo API integration with managed OAuth for accessing and managing profiles, lists, segments, campaigns, flows, events, metrics, templates, catalogs, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing operators use this skill to work with Klaviyo customer data, campaigns, flows, events, analytics, templates, catalogs, and webhooks through Maton-managed OAuth. It is suited for agents that need to read Klaviyo account state or prepare guarded create, update, delete, send, webhook, subscription, or bulk operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and connected Klaviyo OAuth access, which can expose sensitive customer and marketing data if mishandled. <br>
Mitigation: Keep MATON_API_KEY secret, install only when the publisher and connected account scope are trusted, and use narrow reads with sparse fields where possible. <br>
Risk: Write, send, webhook, subscription, and bulk operations can change Klaviyo resources or customer engagement behavior. <br>
Mitigation: Require explicit confirmation of the resource name, resource ID, and intended effect before any create, update, delete, send, webhook, subscription, or bulk operation. <br>
Risk: Agents with multiple Klaviyo connections may operate on the wrong account. <br>
Mitigation: Use the Maton-Connection header when multiple accounts exist and confirm the intended connection before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/klaviyo) <br>
- [Klaviyo API Documentation](https://developers.klaviyo.com) <br>
- [Klaviyo API Reference](https://developers.klaviyo.com/en/reference/api_overview) <br>
- [Klaviyo Developer Portal](https://developers.klaviyo.com/en) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API endpoint descriptions, JSON examples, and inline Python, JavaScript, curl, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, Klaviyo OAuth connection scope, and Klaviyo revision headers.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
