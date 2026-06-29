## Description: <br>
Aggregates LLM usage CSV or Excel logs by provider, model, user, and internal or external user type, then calculates costs from a pricing configuration and writes an Excel report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[no7dw](https://clawhub.ai/user/no7dw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and finance analysts use this skill to summarize authorized LLM usage exports, separate internal and external consumption, identify unpriced models, and calculate cost by provider, model, and user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage inputs and generated Excel reports can contain email addresses, phone numbers, or user IDs. <br>
Mitigation: Process only usage logs you are authorized to handle, and redact or restrict sharing of generated reports outside the intended team. <br>
Risk: Unconfigured or mismatched model pricing can cause affected rows to be reported with zero cost. <br>
Mitigation: Review the terminal validation messages and update pricing_config.json before relying on the report for billing or chargeback decisions. <br>


## Reference(s): <br>
- [Pricing configuration](references/pricing_config.json) <br>
- [ClawHub skill page](https://clawhub.ai/no7dw/skills/llm-usage-aggregator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Analysis, Text] <br>
**Output Format:** [Excel workbook (.xlsx) plus terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-supplied CSV or Excel usage logs and an optional pricing JSON; the workbook contains summary and pricing-detail sheets.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
