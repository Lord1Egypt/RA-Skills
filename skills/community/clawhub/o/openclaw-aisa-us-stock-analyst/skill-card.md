## Description: <br>
Professional US stock analysis with financial data, news, social sentiment, and multi-model AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to gather US equity data, news, social sentiment, and multi-model AI analysis for stock research, portfolio monitoring, earnings review, and screening workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols, watchlists, research queries, prompts, and the AIsa bearer token are sent to AIsa services and may reach downstream model providers. <br>
Mitigation: Do not include confidential account details or proprietary trading strategy in prompts, and use the skill only when this data sharing is acceptable. <br>
Risk: AISA_API_KEY is required for API access. <br>
Mitigation: Protect the API key, avoid committing it to files, and rotate it if exposure is suspected. <br>
Risk: Saved JSON reports may contain raw news, social, financial, and AI analysis data. <br>
Mitigation: Review saved reports before sharing, storing, or using them in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-us-stock-analyst) <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa Documentation](https://aisa.mintlify.app) <br>
- [AIsa Website](https://aisa.one) <br>
- [OpenClaw Homepage](https://openclaw.ai) <br>
- [README](README.md) <br>
- [SKILL](SKILL.md) <br>
- [Test Report](TEST_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON reports] <br>
**Output Format:** [Markdown instructions with Python examples, shell commands, and structured JSON stock-analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY. Reports may include raw financial, news, social, and AI analysis data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
