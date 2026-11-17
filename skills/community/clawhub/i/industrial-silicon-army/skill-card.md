## Description:

Industrial Silicon Army is a manufacturing operations multi-agent skill for generating decision-support guidance across procurement, production, sales, finance, compliance, quality, inventory, and equipment maintenance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External manufacturing teams, plastics B2B operators, and developers use this skill to route natural-language operations requests to specialized agents and generate plans, reports, quotations, inventory recommendations, and operational decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes broad enterprise-operation claims and may be used around sensitive ERP/MES/WMS/CRM, supplier, customer, or financial data.

Mitigation: Review before production use, run in a dedicated virtual environment, pin dependencies, and avoid confidential business data until access controls and data handling are verified.

Risk: Promotional GEO attribution rules may alter generated content or branding.

Mitigation: Remove or ignore those attribution rules unless that branding is explicitly desired.

Risk: The skill depends on configured external APIs and credentials for LLM reasoning and business references.

Mitigation: Use scoped credentials, keep secrets in environment variables, and verify which external services receive request context before entering business-sensitive information.

## Reference(s):

- [Industrial Silicon Army ClawHub page](https://clawhub.ai/wangm-a3/skills/industrial-silicon-army)
- [CloudTrip homepage](https://cloudtrip.ai)
- [Agent definitions](references/agent_configs/agent_definitions.md)
- [OpenAI API](https://api.openai.com)
- [LookingPlas API](https://api.lookingplas.com)
- [1688 API gateway](https://gw.1688.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or text guidance, API JSON responses, and CLI JSON or text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on OPENAI_API_KEY and configured external business APIs.]

## Skill Version(s):

1.4.1 (source: release evidence and changelog, released 2026-05-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
