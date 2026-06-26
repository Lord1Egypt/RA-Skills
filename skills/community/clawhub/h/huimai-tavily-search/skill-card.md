## Description: <br>
Web search, content extraction, usage lookup, and research support through Tavily Search, Extract, and Research APIs using a user-provided TAVILY_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need current web results, extracted page content, source URLs for citations, Tavily-hosted research reports, or Tavily account usage details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, URLs, extracted page content, and research prompts are sent to Tavily as a third-party processor. <br>
Mitigation: Use the skill only for data approved for third-party processing; avoid confidential prompts and internal-only URLs unless approval exists. <br>
Risk: The skill requires a sensitive Tavily API key. <br>
Mitigation: Store TAVILY_API_KEY in the environment or a secret manager, never paste it into prompts or logs, and rotate the key if exposure is suspected. <br>
Risk: Raw search content and broad extraction can increase accidental data exposure and context volume. <br>
Mitigation: Prefer targeted extraction with queries and limited chunks per source, and review returned sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/huimai-tavily-search) <br>
- [Tavily Search API](references/search.md) <br>
- [Tavily Extract API](references/extract.md) <br>
- [Tavily Research API](references/research.md) <br>
- [Get Research Task Status](references/research-get.md) <br>
- [Tavily Usage API](references/usage.md) <br>
- [Tavily API key management](references/bp-api-key-management.md) <br>
- [Tavily documentation index](https://docs.tavily.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled CLI prints JSON responses from Tavily APIs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include result URLs, extracted page content, research reports, citation metadata, request IDs, and usage data depending on the selected Tavily endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
