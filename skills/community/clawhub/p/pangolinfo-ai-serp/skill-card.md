## Description: <br>
Guides agents in using Pangolinfo MCP tools to retrieve Google SERP results, AI Overview or AI Mode output, citations, screenshots, and Google Trends keyword comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangolinfo](https://clawhub.ai/user/pangolinfo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to ground answers in current Google SERP and AI Overview results, compare keyword trends, and present cited search or trend findings. It is intended for Google search, AI search, and trend workflows rather than Amazon site search or deep website crawling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a sensitive Pangolinfo API key. <br>
Mitigation: Install only in environments where granting Pangolinfo MCP access to PANGOLINFO_API_KEY is acceptable, and avoid exposing the key in prompts, logs, or generated reports. <br>
Risk: The release evidence reports inconsistent API-key handling guidance. <br>
Mitigation: Confirm the active credential path before use, and publish one clear credential flow for the skill and MCP server. <br>
Risk: The bundled behavior includes broader Amazon and WIPO Pangolinfo workflows beyond the declared Google SERP and trends purpose. <br>
Mitigation: Use this skill only for Google SERP, AI Overview or AI Mode, and keyword-trend workflows unless the publisher explicitly scopes and documents the broader workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pangolinfo/pangolinfo-ai-serp) <br>
- [Pangolinfo publisher profile](https://clawhub.ai/user/pangolinfo) <br>
- [Pangolinfo service](https://www.pangolinfo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, bullet summaries, citations, and MCP tool-call argument examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Google result URLs, AI Overview citations, relative trend summaries, and screenshot references when returned by the tool.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
