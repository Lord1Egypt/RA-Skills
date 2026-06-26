## Description: <br>
Free, unlimited web search for AI agents via SearXNG -- no API keys needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choihyunsus](https://clawhub.ai/user/choihyunsus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to add web, news, image, video, and suggestion search through a SearXNG-based MCP server without managing search API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public-mode searches may disclose sensitive prompts, URLs, or business context to external search infrastructure. <br>
Mitigation: Use the self-hosted SEARXNG_URL mode for sensitive research and avoid entering passwords, tokens, personal data, internal URLs, or confidential business details into public-mode searches. <br>
Risk: The skill runs an npm package through npx, so users depend on the package and publisher supply chain. <br>
Mitigation: Install only after reviewing and trusting the n2-free-search npm package and publisher, and pin or mirror package versions where deployment policy requires it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/choihyunsus/n2-free-search) <br>
- [NPM Package](https://www.npmjs.com/package/n2-free-search) <br>
- [Project Repository](https://github.com/choihyunsus/n2-free-search) <br>
- [Project Website](https://nton2.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return web, news, image, video, and suggestion search results depending on the invoked MCP tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
