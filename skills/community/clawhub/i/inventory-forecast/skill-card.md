## Description:

Projects inventory needs from historical order velocity, seasonality, supplier lead times, and planned promotions so ecommerce teams can reorder before stockouts hurt rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and inventory planners use this skill to calculate reorder points, plan promotional stock, build reorder calendars, and compare sell-through across SKUs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecasting may involve sensitive business data such as SKU sales history, stock levels, supplier lead times, planned promotions, and purchase-order costs.

Mitigation: Review data handling before use and share only the inventory and planning fields needed for the forecast.

Risk: Reorder, markdown, and freight recommendations can be wrong if assumptions, missing data, or benchmark substitutions are not reviewed.

Mitigation: Review the stated assumptions, output checklist, and forecast tables before acting on purchasing, markdown, or freight decisions.

## Reference(s):

- [Inventory Forecast - Output Template](references/output-template.md)
- [Demand Forecasting Methods](references/demand-forecasting-methods.md)
- [Lead Time & Safety Stock Reference](references/lead-time-and-safety-stock.md)
- [Forecast Quality Checklist](assets/forecast-quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown forecast report with tables, assumptions, reorder calendar, and action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided sales, inventory, supplier, promotion, MOQ, and case-pack data; outputs assumptions and quality checks.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
