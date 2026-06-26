## Description: <br>
Tsearch Web Search lets agents query LinkFox web search and summarize extracted result content for current information, news, Reddit and community discussions, trends, product reviews, and competitor research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current web information through LinkFox Tsearch and summarize extracted result content with source titles and URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are sent to LinkFox and may contain sensitive prompts, secrets, customer data, or personal details. <br>
Mitigation: Use the skill only when sending the query to LinkFox is acceptable, and redact sensitive content before searching. <br>
Risk: The skill asks agents to automatically report feedback containing user intent to LinkFox. <br>
Mitigation: Do not submit feedback without explicit user approval, and redact private prompts, secrets, customer data, and personal details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-tsearch-web-search) <br>
- [Web Search API Reference](references/api.md) <br>
- [Tsearch Search API endpoint](https://tool-gateway.linkfox.com/tsearch/search) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries with source titles and URLs; API responses are JSON with searchList results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses one keyword string up to 1000 characters and returns extracted page content with a costToken value.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
