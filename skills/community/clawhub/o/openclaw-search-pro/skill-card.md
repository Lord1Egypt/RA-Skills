## Description: <br>
OpenClaw Search Pro gives agents multi-engine web search and URL content extraction with free engines plus optional Tavily, Baidu, Google, and Bing API configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwg2025](https://clawhub.ai/user/williamwg2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search the web across multiple engines, retrieve recent information, and extract readable content from URLs during agent research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to external search providers. <br>
Mitigation: Do not search secrets, internal project names, customer data, or other confidential terms unless the provider and network path are approved. <br>
Risk: The URL extractor should not be treated as a complete SSRF or private-network barrier. <br>
Mitigation: Extract only from trusted public URLs and review network controls before use in restricted environments. <br>
Risk: Optional API keys may be stored in local configuration. <br>
Mitigation: Prefer environment variables, restrict config file permissions, and keep credentials out of source control. <br>
Risk: Documentation contains conflicting claims about network behavior. <br>
Mitigation: Treat the skill as network-enabled and review it before installing in confidential or restricted-network environments. <br>


## Reference(s): <br>
- [OpenClaw Search Pro ClawHub page](https://clawhub.ai/williamwg2025/openclaw-search-pro) <br>
- [README.md](artifact/README.md) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [Baidu API Guide](artifact/BAIDU-API-GUIDE.md) <br>
- [Baidu Search API](https://ai.baidu.com/tech/search) <br>
- [Baidu Search API Documentation](https://ai.baidu.com/ai-doc/SEARCH) <br>
- [Bing Web Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands] <br>
**Output Format:** [Terminal text with ranked search results, URLs, snippets, engine labels, and extracted page excerpts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include third-party web content and should be reviewed before reuse.] <br>

## Skill Version(s): <br>
0.1.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
