## Description: <br>
Search the web and X (Twitter) using xAI's Grok API with real-time access, citations, and image understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[castanley](https://clawhub.ai/user/castanley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to retrieve current web information and X discussion through xAI's Grok API, including source citations and optional media understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, filters, and media-analysis inputs are sent to xAI. <br>
Mitigation: Avoid submitting secrets, regulated data, or confidential business information in searches. <br>
Risk: The skill requires an xAI API key for API calls. <br>
Mitigation: Use a dedicated API key that can be monitored, rotated, and revoked. <br>
Risk: Reasoning searches and optional media understanding can add latency and API cost. <br>
Mitigation: Enable media understanding only when needed and narrow searches with domains, handles, or date ranges. <br>


## Reference(s): <br>
- [xAI Web Search documentation](https://docs.x.ai/developers/tools/web-search) <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI API base](https://api.x.ai/v1) <br>
- [xAI API console](https://console.x.ai/) <br>
- [ClawHub skill page](https://clawhub.ai/castanley/grok) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, api calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text responses with citations, usage metadata, and optional JSON-like result objects from API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY; supports web and X search filters, date ranges, and optional image or video understanding.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
