## Description: <br>
Search the live web through Moonshot's builtin $web_search tool and return a concise answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fusae](https://clawhub.ai/user/fusae) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route live web search, current-information lookup, and online verification through Moonshot when direct browser-style source extraction is not required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Moonshot with the configured API key. <br>
Mitigation: Avoid putting secrets or private data in search queries and install only when Moonshot is the intended search provider. <br>
Risk: Search-result grounding may be incomplete, especially when citations or strict factual sourcing matter. <br>
Mitigation: Validate important answers against another source or use a browser/search workflow that can provide exact links and page-level attribution. <br>
Risk: Persistent routing rules may cause live web searches to use this third-party service by default. <br>
Mitigation: Review any OpenClaw TOOLS.md routing rule before adding it and make sure the routing behavior matches user and workspace expectations. <br>


## Reference(s): <br>
- [Moonshot Web Search ClawHub Listing](https://clawhub.ai/fusae/moonshot-web-search) <br>
- [Moonshot Search Skill Homepage](https://github.com/fusae/moonshot-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text answer from the Moonshot search script, optionally summarized by the agent in the user's requested style.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOONSHOT_API_KEY and sends search queries to Moonshot; use a browser or search workflow instead when exact citations, links, or page-level attribution are required.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
