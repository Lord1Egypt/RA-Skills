## Description: <br>
AI-optimized web search via AIsa's Tavily API proxy. Returns concise, relevant results for AI agents through AIsa's unified API gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to run web searches and extract public URL content through AIsa's Tavily gateway, with options for result count, deep search, general or news topics, and news recency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and requested URLs are sent to AIsa/Tavily using the user's AISA_API_KEY. <br>
Mitigation: Use a dedicated key where possible, avoid confidential internal URLs, private network targets, signed links, or customer-specific resources, and keep the API key out of logs and shared environments. <br>
Risk: URL extraction can be misused to retrieve paywalled, subscription-gated, or otherwise access-controlled content. <br>
Mitigation: Extract only content the user is authorized to access, refuse paywall circumvention, and direct users to subscriptions, institutional access, or public alternatives. <br>
Risk: Redundant or excessive searches can waste API quota and create service-abuse patterns. <br>
Mitigation: Consolidate overlapping requests into two or three focused queries before running the search command. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/snazar-faberlens/openclaw-aisa-web-search-tavily-hardened) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa API key marketplace](https://marketplace.aisa.one) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/openclaw-aisa-web-search-tavily) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown sections containing answers, source lists, extracted URL content, and failed URL notices.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and AISA_API_KEY; search results are capped at 20 per query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
