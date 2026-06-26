## Description: <br>
财搭子是一个投资研究 Agent，可调用外部 API 识别资产并生成财务、估值、技术面、资金面和市场情绪分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunlujing](https://clawhub.ai/user/sunlujing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual investors, analysts, and investment advisors use this skill to turn natural-language stock questions into quick overviews, single-dimension analysis, or multi-dimension research reports. It supports asset extraction, comparison, and investment research workflows across financial, valuation, technical, capital-flow, and market-sentiment dimensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance queries, asset identifiers, and related prompt content are sent to the provider's external API. <br>
Mitigation: Use the skill only when that data sharing is acceptable, avoid including sensitive personal or account details, and review the provider relationship before deployment. <br>
Risk: The API token is a bearer credential required for access. <br>
Mitigation: Store TOOL_API_TOKEN only in a secret manager or local environment, never commit it to files, and rotate it if exposure is suspected. <br>
Risk: Overriding TOOL_API_URL can redirect requests and token-bearing traffic to another endpoint. <br>
Mitigation: Leave TOOL_API_URL at the default unless you intentionally control and trust the replacement HTTPS endpoint. <br>
Risk: Investment reports can be time-sensitive and may be inappropriate as sole decision support. <br>
Mitigation: Treat outputs as research support, verify key figures against authoritative sources, and preserve the skill's risk and data-timeliness notices in user-facing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunlujing/invest-buddy) <br>
- [Investment research API endpoint](https://api.facaidazi.com/api/tools/call) <br>
- [tool-client-usage.md](references/tool-client-usage.md) <br>
- [tool-specs.md](references/tool-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional JSON API responses and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOL_API_TOKEN; TOOL_API_URL can override the default HTTPS endpoint.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
