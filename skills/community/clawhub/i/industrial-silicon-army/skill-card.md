## Description: <br>
Industrial Silicon Army is a manufacturing-focused multi-agent assistant for factory management, supply-chain planning, quality control, predictive maintenance, quotation support, and operational reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing operators, supply-chain teams, and developers use this skill to route natural-language factory, procurement, sales, finance, compliance, and reporting tasks to specialized agents that generate advisory plans, quotations, reports, and API-backed responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive business credentials and may send prompts or business data to configured external APIs. <br>
Mitigation: Confirm which APIs receive data before installation, use least-privilege credentials, and start with non-production ERP, CRM, OAuth, and API keys. <br>
Risk: Procurement, payment, account, customer-credit, compliance, and supplier outputs can affect business commitments if acted on automatically. <br>
Mitigation: Keep purchasing, payment, account changes, data exports, and supplier decisions behind explicit human approval. <br>
Risk: Financial, customer-credit, compliance, and supplier guidance may be incomplete, stale, or incorrect. <br>
Mitigation: Treat these outputs as advisory and require responsible business, finance, or compliance review before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangm-a3/industrial-silicon-army) <br>
- [Publisher profile](https://clawhub.ai/user/wangm-a3) <br>
- [CloudTrip homepage](https://cloudtrip.ai) <br>
- [OpenAI API](https://api.openai.com) <br>
- [LookingPlas API](https://api.lookingplas.com) <br>
- [1688 API gateway](https://gw.1688.com) <br>
- [Agent definitions](references/agent_configs/agent_definitions.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON responses, with optional shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and may include procurement, inventory, production, quality, finance, compliance, and reporting recommendations.] <br>

## Skill Version(s): <br>
1.4.1 (source: server-resolved release metadata and changelog, released 2026-05-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
