## Description: <br>
节假日出行决策skill generates Chinese holiday travel decision reports with off-peak travel windows, leave-day suggestions, budget ranges, destination judgments, and next actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyikoi](https://clawhub.ai/user/keyikoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users planning China public-holiday travel use this skill to decide whether and when to travel, which leave days to request, which destinations to prefer or avoid, and what budget range to expect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The visual report widget may load Chart.js from jsDelivr. <br>
Mitigation: Use a locally bundled chart library, subresource integrity, and sandboxed widget rendering in stricter environments. <br>
Risk: Travel costs and holiday advice are not live booking data. <br>
Mitigation: Verify prices, availability, dates, and local conditions with current authoritative sources before acting on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keyikoi/holiday-exodus-planner) <br>
- [Evaluation rules](references/evaluation_rules.md) <br>
- [Report template](references/report_template.md) <br>
- [Widget data spec](references/widget_data_spec.md) <br>
- [Example report](references/example_report.md) <br>
- [Holiday data](assets/holidays.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Chinese Markdown decision report plus JSON-compatible widget data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured data for visual rendering with assets/report_widget.html.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
