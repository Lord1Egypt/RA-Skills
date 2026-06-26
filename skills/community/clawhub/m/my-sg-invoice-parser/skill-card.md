## Description: <br>
Extract structured data from Malaysian and Singaporean invoices and receipts, with SST/GST-aware tax guidance for Bahasa Malaysia, English, and Chinese inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wms2537](https://clawhub.ai/user/wms2537) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to prepare structured invoice or receipt JSON for Malaysia and Singapore, including local SST/GST detection and tax calculations. The hosted endpoint is used for SkillPay billing authorization and tax-rate retrieval before the agent performs extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan reports that the executable code charges a user before doing invoice parsing or explicit per-call confirmation. <br>
Mitigation: Use the skill only when the agent obtains explicit user approval for each paid call and discloses the $0.02 USDT SkillPay charge before sending the request. <br>
Risk: ClawScan characterizes the release as a paid billing and tax-rate helper rather than a self-contained invoice parser. <br>
Mitigation: Treat endpoint results as billing status and tax-rate data only; the agent should perform and validate invoice extraction separately. <br>
Risk: Security guidance notes that calls send user_id and country to the hosted endpoint. <br>
Mitigation: Send only the required user_id and country after user approval, and avoid including invoice contents or additional personal data in the endpoint request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wms2537/my-sg-invoice-parser) <br>
- [Publisher profile](https://clawhub.ai/user/wms2537) <br>
- [Project homepage](https://github.com/swmeng/myskills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON] <br>
**Output Format:** [Markdown instructions and JSON examples for structured invoice data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLPAY_API_KEY for the hosted billing and tax-rate endpoint.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
