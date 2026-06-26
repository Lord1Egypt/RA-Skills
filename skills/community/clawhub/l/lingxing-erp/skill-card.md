## Description: <br>
领星 ERP integrates OpenClaw with Lingxing ERP to query order data, with configuration for Lingxing API credentials and endpoint selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wengjianmin19850412](https://clawhub.ai/user/wengjianmin19850412) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Lingxing ERP and retrieve today's order data through the configured Lingxing OpenAPI credentials. The artifact describes inventory and product-list use cases, but this release's executable implementation exposes only the today-orders function. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Lingxing ERP API credentials and can send requests to the configured BASE_URL. <br>
Mitigation: Use least-privilege Lingxing keys, keep credentials out of prompts and logs, and keep BASE_URL pointed to the official or another trusted Lingxing endpoint. <br>
Risk: The release description advertises inventory and product-list queries that are not implemented in the executable artifact. <br>
Mitigation: Treat this version as an order-query skill unless the missing functions are added and reviewed in a later release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wengjianmin19850412/lingxing-erp) <br>
- [Publisher profile](https://clawhub.ai/user/wengjianmin19850412) <br>


## Skill Output: <br>
**Output Type(s):** [JSON] <br>
**Output Format:** [JSON object returned from the Lingxing ERP API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns paginated order data for the current local date; exact fields depend on the Lingxing ERP API response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
