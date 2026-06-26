## Description: <br>
Web search via KokoChat's hosted Brave-backed search proxy without requiring a search API key on the user's machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[komako-workshop](https://clawhub.ai/user/komako-workshop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to let an OpenClaw agent retrieve web search results through KokoChat's hosted Brave-backed proxy without configuring local search credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to KokoChat's deeply.plus hosted search service. <br>
Mitigation: Install only when this data flow is acceptable; avoid sending sensitive queries and require explicit invocation if generic search triggers are too broad. <br>


## Reference(s): <br>
- [KokoChat Search ClawHub release](https://clawhub.ai/komako-workshop/kokochat-search) <br>
- [KokoChat hosted search endpoint](https://deeply.plus/deeply/search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands, guidance] <br>
**Output Format:** [JSON search response with status, provider, query metadata, and result title, URL, and snippet entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a query string and optional count; queries are trimmed to 500 characters and results are limited to 1-10 normalized HTTP(S) entries.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
