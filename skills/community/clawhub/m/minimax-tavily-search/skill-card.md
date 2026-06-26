## Description: <br>
AI-optimized web search via Tavily API. Returns concise, relevant results for Minimax AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenchao2046](https://clawhub.ai/user/wenchao2046) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily web searches and extract clean content from selected URLs for research, current-events lookup, and source gathering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and selected URLs are sent to Tavily with a Tavily API key. <br>
Mitigation: Use a dedicated API key where possible and avoid submitting secrets, private data, or internal URLs. <br>
Risk: Returned search results and extracted web content may be incomplete, outdated, or untrusted. <br>
Mitigation: Review returned sources before relying on them and verify important claims against authoritative references. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wenchao2046/minimax-tavily-search) <br>
- [Publisher Profile](https://clawhub.ai/user/wenchao2046) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with headings, source links, relevance scores, extracted page content, and failed URL summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; search results are capped at 20.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
