## Description: <br>
Search the web with Google Search grounding for current events, documentation, real-time data, news, or information that may have changed recently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daanielcruz](https://clawhub.ai/user/daanielcruz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Google-backed web searches when freshness, citations, and source URLs matter. It is suitable for MCP-compatible agent workflows that need current web information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external package uses Google or Gemini authentication, including sensitive OAuth credentials, and the skill text does not fully explain that behavior. <br>
Mitigation: Install only if you trust the @daanielcruz/gsearch-mcp package, review the OAuth consent flow, prefer a dedicated Google account or explicit API key, and isolate existing Gemini CLI credentials if they should not be reused. <br>
Risk: Search queries may expose sensitive user, business, or project information to external search and authentication services. <br>
Mitigation: Avoid sensitive search queries and review generated source links and citations before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daanielcruz/gsearch) <br>
- [GSearch MCP homepage](https://github.com/daanielcruz/gsearch-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline citations, source URLs, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search responses should keep returned citations and list source URLs; typical response time is 2-15 seconds and may reach 60 seconds with retries.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
