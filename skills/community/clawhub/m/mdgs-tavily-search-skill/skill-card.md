## Description: <br>
Uses the Tavily API to search the web, extract page content, crawl sites, map site structure, and run research tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[343195246](https://clawhub.ai/user/343195246) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need web search, page extraction, site crawling, site mapping, or multi-source research through Tavily. It helps choose the appropriate Tavily mode and provides command-line and JavaScript examples for invoking it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, crawl instructions, and research prompts are sent to Tavily and may reach external websites. <br>
Mitigation: Use only queries and URLs approved for third-party sharing, and avoid secrets, internal URLs, personal data, or regulated content unless that sharing is acceptable. <br>
Risk: Crawl and research modes can broaden outbound requests and collect more source material than intended. <br>
Mitigation: Set explicit depth, page, result, and source limits before use, and review returned content before relying on it. <br>
Risk: The skill requires a Tavily API key. <br>
Mitigation: Provide the key through the TAVILY_API_KEY environment variable and do not hardcode it in prompts, scripts, or shared files. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Documentation](https://docs.tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript examples, and text or JSON-shaped Tavily responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY and supports mode-specific limits such as search depth, max results, max pages, and max sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
