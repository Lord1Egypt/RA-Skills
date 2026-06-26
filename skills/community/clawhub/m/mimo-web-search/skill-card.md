## Description: <br>
Uses Xiaomi MiMo's web search-enabled model to retrieve current web information for user queries with a configured API key and paid API usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EnderXiao](https://clawhub.ai/user/EnderXiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to answer time-sensitive questions and cross-check information by sending search queries to Xiaomi MiMo's web search API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted search query could exploit the shell-based curl implementation to run local commands. <br>
Mitigation: Do not use on sensitive machines until the implementation uses a safe HTTPS client or argument-based subprocess calls; keep the MiMo API key limited. <br>
Risk: Search queries and results are sent to Xiaomi's MiMo service and may be billed. <br>
Mitigation: Avoid sensitive queries, monitor paid usage, and cache repeated searches where appropriate. <br>
Risk: Raw prompts, search results, or API errors could expose sensitive information through logs. <br>
Mitigation: Avoid logging raw queries or results and redact operational logs before sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EnderXiao/mimo-web-search) <br>
- [README.md](artifact/README.md) <br>
- [USAGE.md](artifact/USAGE.md) <br>
- [MiMo Chat Completions API Endpoint](https://api.xiaomimimo.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown search summaries or JSON-like result objects with content, usage, citations, and errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MIMO_API_KEY, sends queries to Xiaomi MiMo, and may incur paid API charges.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
