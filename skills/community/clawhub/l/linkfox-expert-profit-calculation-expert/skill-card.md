## Description:

利润核算专家 helps Amazon sellers evaluate ASIN profitability by combining marketplace fees, sourcing costs, return-rate assumptions, advertising costs, storage fees, and inbound fees into an HTML profit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this skill to compare candidate ASINs, test cost assumptions, and generate a profit report before sourcing or listing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product research, images, ASINs, prompts, and account-authenticated requests to LinkFox services.

Mitigation: Use the skill only with data approved for LinkFox processing, and avoid entering sensitive business strategy or credentials in prompts.

Risk: Configurable LinkFox gateway or login endpoints could expose account credentials if pointed at an untrusted service.

Mitigation: Keep endpoints at trusted defaults or set custom endpoint environment variables only for services you control and trust.

Risk: Persistent memory and feedback behavior may retain or report task context.

Mitigation: Review or disable feedback and MEMORY.md behavior where possible, especially for sensitive sourcing assumptions or supplier decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-profit-calculation-expert)
- [Workflow](artifact/skills/profit-calculation-expert/references/workflow.md)
- [Output Schema](artifact/skills/profit-calculation-expert/references/output-schema.md)
- [Data Fields](artifact/skills/profit-calculation-expert/references/data-fields.md)
- [FBA Fee Table](artifact/skills/profit-calculation-expert/references/fba-fee-table.md)
- [Report Template](artifact/skills/profit-calculation-expert/references/report-template.md)

## Skill Output:

**Output Type(s):** [text, HTML, JSON, guidance]

**Output Format:** [HTML report with summary text and intermediate JSON profit data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include profitability ranking, cost breakdowns, supplier match details, and data-source notes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
