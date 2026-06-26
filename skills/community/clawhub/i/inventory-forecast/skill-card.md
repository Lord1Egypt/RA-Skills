## Description: <br>
Project inventory needs based on historical order velocity, seasonality, supplier lead times, and planned promotions so you reorder before stockouts hurt rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecommerce operators, inventory planners, and agents supporting sellers use this skill to forecast SKU demand, calculate reorder points and quantities, plan promotion stock, build reorder calendars, and identify overstock actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive sales, inventory, supplier, promotion, and cash-planning data. <br>
Mitigation: Use the skill only with data the user is authorized to share, avoid unnecessary sensitive detail, and keep forecast outputs in approved business systems. <br>
Risk: Forecasts can produce reorder, markdown, air-freight, or cash-outlay recommendations that affect purchasing and operations. <br>
Mitigation: Treat outputs as planning guidance; require human review and approval before placing purchase orders, changing promotions, markdowns, or logistics plans. <br>
Risk: Missing or low-quality sales history, lead-time data, or promotion history can make recommendations overconfident. <br>
Mitigation: State assumptions and data gaps, flag benchmark substitutions, run the included quality checklist, and rerun the forecast when velocity, lead time, promo plans, or inbound shipments change. <br>


## Reference(s): <br>
- [Inventory Forecast ClawHub Release](https://clawhub.ai/leooooooow/inventory-forecast) <br>
- [Output Template](references/output-template.md) <br>
- [Demand Forecasting Methods](references/demand-forecasting-methods.md) <br>
- [Lead Time & Safety Stock Reference](references/lead-time-and-safety-stock.md) <br>
- [Forecast Quality Checklist](assets/forecast-quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown forecast report with tables, assumptions, reorder calendar, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include reorder quantities, safety-stock calculations, last-safe-order dates, PO cash-outlay timelines, and overstock action plans.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
