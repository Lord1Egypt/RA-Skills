## Description: <br>
Analyzes meme-token names with recent web sentiment and LLM scoring to produce a four-part rating report for tokens such as PEPE, DOGE, and SHIB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate meme and community token narratives, sentiment, risk signals, and data freshness before generating a non-investment-advice rating report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence rates this release as suspicious because the package contains mismatched implementation paths and risky local helper or API surfaces. <br>
Mitigation: Review the package before installing, restrict execution in sensitive workspaces, and confirm that the included service code is intended for the deployment environment. <br>
Risk: The skill sends token queries to external search, LLM, and image services. <br>
Mitigation: Avoid entering private watchlists, wallet identifiers, credentials, proprietary research terms, or other sensitive data. <br>
Risk: Security guidance calls out eval-based environment scripts and raw request-body logging as items to restrict before sensitive use. <br>
Mitigation: Remove or limit eval-based environment scripts, disable raw request-body logging, and confirm whether image generation is intended before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deanpeng-dotcom/meme-token-analyzer) <br>
- [Metadata Repository](https://github.com/AntalphaAI/meme-token-analyzer) <br>
- [MCP Server](https://mcp-skills.ai.antalpha.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style analysis report with rating labels, source links, freshness notes, and disclaimer text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a token name and an agent_id from the Antalpha registration flow.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
