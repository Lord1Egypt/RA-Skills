## Description: <br>
Matches an insurance product name to the appropriate product version and returns detailed product parameters and configuration information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangbaiqi521](https://clawhub.ai/user/wangbaiqi521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance advisors, support teams, and external users can query an insurance product by name to retrieve product details. The skill maps the product name to product identifiers, handles multiple matched versions by selecting and disclosing the chosen match, and returns the API result for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected insurance product identifiers are sent to an external product-detail API. <br>
Mitigation: Install only when that external API use is acceptable and avoid submitting sensitive user data beyond the product identifiers needed for lookup. <br>
Risk: Insurance product details returned by the API may be incomplete, stale, or inconsistent with official policy documents. <br>
Mitigation: Confirm important coverage, pricing, exclusions, and policy terms against official insurance documentation before relying on the result. <br>
Risk: Product-name matching depends on a trusted product-mapping CSV, and multiple versions may resolve to the first match. <br>
Mitigation: Use a trusted mapping file and review the disclosed matched product version when the input name is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangbaiqi521/product-detail-query) <br>
- [Product detail API endpoint](https://openapi-test.hongdibaobei.com/v1/chat/robot/product/detail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Markdown summary with JSON API output where appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses productCode and secondTypeId parameters derived from product-name mapping.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
