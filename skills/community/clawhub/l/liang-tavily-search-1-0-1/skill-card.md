## Description: <br>
Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TerryRen2024](https://clawhub.ai/user/TerryRen2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily web searches, retrieve ranked source snippets and metadata, and optionally request news, recency, domain filtering, deeper search, raw content, or raw JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and selected search options are sent to Tavily. <br>
Mitigation: Avoid including secrets, private documents, or sensitive personal data in queries unless that matches the user's data-handling requirements. <br>
Risk: The skill requires a Tavily API key. <br>
Mitigation: Provide the key through TAVILY_API_KEY or trusted OpenClaw configuration and avoid sharing it in prompts, search queries, or public files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TerryRen2024/liang-tavily-search-1-0-1) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Markdown source list with optional answer text, or raw JSON when --json is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; result count is clamped to 1-20.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
