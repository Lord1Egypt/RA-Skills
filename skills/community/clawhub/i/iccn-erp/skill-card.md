## Description: <br>
Provides ERP business-data lookup guidance for the Zero One Wenjie IC ERP foreign trade management system, including orders, purchases, demand records, warehouse movements, customers, suppliers, and inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jexm](https://clawhub.ai/user/jexm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees or agents supporting ERP operations use this skill to map natural-language business queries to the appropriate ERP table and request parameters, then summarize returned ERP records for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ERP lookups can expose sensitive business records if the endpoint or token is overbroad or untrusted. <br>
Mitigation: Use only a trusted ERP_API_BASE_URL and a read-only, least-privilege ERP_API_TOKEN scoped to authorized users and records. <br>
Risk: Broad or ambiguous queries may return more customer, supplier, order, or inventory data than intended. <br>
Mitigation: Confirm ambiguous requests, prefer specific filters, and treat all returned ERP data as confidential. <br>


## Reference(s): <br>
- [Order Detail UI Reference](references/order-detail-ui.md) <br>
- [ClawHub skill page](https://clawhub.ai/jexm/iccn-erp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown, Code] <br>
**Output Format:** [Markdown guidance with JavaScript request examples and tabular ERP results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ERP_API_TOKEN and ERP_API_BASE_URL environment variables. Returned ERP data should be treated as confidential.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
