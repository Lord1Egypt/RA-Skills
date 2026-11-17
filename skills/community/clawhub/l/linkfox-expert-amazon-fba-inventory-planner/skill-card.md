## Description:

Plans Amazon FBA restocks, safety stock, inbound timing, warehouse allocation, and inventory risk checks for Amazon sellers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and operations teams use this skill to turn inventory, sales, lead-time, fee, and capacity data into weekly or monthly FBA restock plans. It supports demand forecasting, safety stock, replenishment quantities, FBA/AWD/hub allocation, aged-inventory decisions, and portfolio-level cash summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle may handle LinkFox API keys for Amazon seller workflows.

Mitigation: Install only when LinkFox service access is intended, avoid storing API keys in shell profiles, and rotate any key that appears in logs.

Risk: Scheduled automation can run inventory workflows without a fresh manual prompt.

Mitigation: Create scheduled tasks only with explicit user intent and review task scope, cadence, and data access before enabling them.

Risk: Public upload behavior can expose sensitive seller reports or inventory files.

Mitigation: Use public uploads only for non-sensitive files and confirm that reports or CSVs do not contain confidential business data before publishing.

Risk: Feedback-reporting behavior may transmit task context outside the local workspace.

Mitigation: Review the feedback-reporting behavior before deployment and avoid submitting secrets, private seller data, or customer data in feedback.

Risk: Incomplete seller inputs can produce misleading purchase or inbound recommendations.

Mitigation: Apply the skill's COMPLETE, DEGRADED, and BLOCKED data contract and do not issue firm purchase order recommendations when sellable inventory or demand signals are missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-amazon-fba-inventory-planner)
- [Amazon FBA Inventory Planning skill](artifact/skills/amazon-fba-inventory-planning/SKILL.md)
- [Wrapper skill routing and workflow](artifact/SKILL.md)
- [Weekly FBA Inventory Plan output guide](artifact/skills/amazon-fba-inventory-planning/assets/weekly-plan-output-guide.md)
- [Data Contract & Missing-Data Degradation](artifact/skills/amazon-fba-inventory-planning/references/data-contract.md)
- [Demand Forecasting for Amazon FBA Inventory Planning](artifact/skills/amazon-fba-inventory-planning/references/demand-forecasting.md)
- [Safety Stock & Reorder Point Guidance for Amazon FBA](artifact/skills/amazon-fba-inventory-planning/references/safety-stock.md)
- [Amazon FBA Fees Reference (2026)](artifact/skills/amazon-fba-inventory-planning/references/fba-fees.md)
- [IPI, Storage Capacity & Restock Limits](artifact/skills/amazon-fba-inventory-planning/references/ipi-capacity-limits.md)
- [Multi-Warehouse & AWD Allocation](artifact/skills/amazon-fba-inventory-planning/references/multi-warehouse.md)
- [Multi-Channel Shared Inventory](artifact/skills/amazon-fba-inventory-planning/references/multi-channel-inventory.md)
- [Ads-Inventory Linkage for FBA Planners](artifact/skills/amazon-fba-inventory-planning/references/ads-inventory-linkage.md)
- [Exception Alerts & Priority Scoring](artifact/skills/amazon-fba-inventory-planning/references/exception-priority.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with SKU-level tables, generated files, JSON or CSV data, and command-backed calculation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route long reports to generated HTML files and may use calculation scripts for forecasts, restock quantities, ATP, priority scores, and hold-versus-remove decisions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
