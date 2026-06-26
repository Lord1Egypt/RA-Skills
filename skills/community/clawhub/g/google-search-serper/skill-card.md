## Description: <br>
Google Search powered by Serper.dev API across web, news, images, videos, places, shopping, scholar, patents, and autocomplete, returning rich search result fields such as Knowledge Graph, Answer Box, People Also Ask, and Related Searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minilozio](https://clawhub.ai/user/minilozio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and their users use this skill to run Google-backed searches through Serper.dev for current web information, news, media, places, shopping, academic papers, patents, and autocomplete suggestions. It is useful when the user asks for Google results or richer search result structure than a basic web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Serper.dev and Google-backed search infrastructure, which may expose sensitive topics if users submit secrets, personal data, regulated information, or confidential business context. <br>
Mitigation: Use a dedicated Serper API key and avoid sending sensitive, regulated, or confidential queries unless that external processing is acceptable for the deployment. <br>
Risk: Searches consume Serper credits, and shopping searches cost more credits than other search types. <br>
Mitigation: Monitor credit balance, use shopping only when the user explicitly asks for prices or shopping results, and keep request volume within the documented service limits. <br>
Risk: Search result snippets and rich result fields can be incomplete, outdated, or inaccurate. <br>
Mitigation: Treat results as leads, verify important claims against the linked sources, and fetch source pages when deeper evidence is needed. <br>


## Reference(s): <br>
- [Serper.dev API Reference](references/serper-api.md) <br>
- [Serper.dev](https://serper.dev) <br>
- [ClawHub Skill Page](https://clawhub.ai/minilozio/google-search-serper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Formatted console text by default, with optional raw JSON when --json is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes search result links, snippets, rich result fields, and credit balance when returned by the API; requires SERPER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
