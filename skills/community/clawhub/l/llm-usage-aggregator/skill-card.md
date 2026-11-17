## Description:

Llm Usage Aggregator summarizes LLM usage CSV or Excel logs by provider, model, user, and internal or external user type, then generates an Excel workbook with cost calculations from a pricing configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[no7dw](https://clawhub.ai/user/no7dw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and finance or analytics teams use this skill to turn LLM usage logs into model, provider, user, and user-type summaries with estimated USD costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input logs and generated workbooks may contain raw user identifiers, usage metrics, and cost data.

Mitigation: Process files locally, restrict access to inputs and generated workbooks, and treat both as sensitive operational data.

Risk: Untrusted CSV or Excel values that begin with =, +, -, or @ may be unsafe when opened or shared in spreadsheet software.

Mitigation: Use trusted input files or sanitize spreadsheet-triggering values before opening or distributing generated workbooks.

Risk: Missing or stale model pricing can cause affected rows to be reported with zero cost.

Mitigation: Review pricing validation warnings and keep references/pricing_config.json current before relying on cost totals.

## Reference(s):

- [pricing_config.json](references/pricing_config.json)
- [ClawHub skill page](https://clawhub.ai/no7dw/skills/llm-usage-aggregator)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated workflow creates a local Excel workbook with summary and pricing-detail sheets.]

## Skill Version(s):

0.1.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
