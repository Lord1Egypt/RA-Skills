## Description: <br>
Compare payment processors on fees, conversion rates, and regional coverage to optimize checkout success rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators, product teams, and developers use this skill to compare gateway fees, payment method coverage, conversion performance, and multi-gateway routing options before changing checkout infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway recommendations may rely on sensitive business inputs such as transaction volume, revenue mix, target markets, and checkout pain points. <br>
Mitigation: Avoid sharing production API keys, secrets, or unnecessarily precise confidential revenue data with the agent; use rounded or sanitized planning data where possible. <br>
Risk: Fee schedules, regional payment method coverage, and gateway capabilities can change after the skill reference material is published. <br>
Mitigation: Verify current gateway pricing, local payment method availability, and compliance requirements before making routing, contract, or checkout infrastructure changes. <br>
Risk: Payment-routing changes can affect checkout conversion, authorization rates, dispute handling, and business continuity. <br>
Mitigation: Use staged rollout, sandbox testing, monitoring, fallback routing, and rollback planning before applying recommendations to production payment flows. <br>


## Reference(s): <br>
- [Output Template](references/output-template.md) <br>
- [Fee Calculation Reference](references/fee-calculation-reference.md) <br>
- [Regional Payment Methods Guide](references/regional-payment-methods.md) <br>
- [Quality Checklist](assets/quality-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/leooooooow/payment-gateway-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown analysis with comparison tables, routing rules, cost models, implementation roadmap, and review checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; users should verify current gateway fees and regional payment method data before making business or payment-routing changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
