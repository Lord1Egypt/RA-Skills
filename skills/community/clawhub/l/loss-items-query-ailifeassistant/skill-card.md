## Description: <br>
查询 待复购商品/ 待购买商品 /资损品物品列表/商品补货，支持分页、状态、排序等参数。直接调用你的业务 HTTPS 接口。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KUNXINIAN](https://clawhub.ai/user/KUNXINIAN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators use this skill to query pending repurchase, purchase, loss-item, or restocking records from a token-protected business API and receive a summarized response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as generic pending or page requests may cause token-backed business-data lookups when the user intent is ambiguous. <br>
Mitigation: Narrow the trigger phrases and require explicit confirmation before querying in shared or sensitive environments. <br>
Risk: The skill retrieves and summarizes loss-item or inventory-related business data using LOSS_API_TOKEN. <br>
Mitigation: Install only where the token is controlled and trusted, and limit token access to the minimum API scope needed for the query. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KUNXINIAN/loss-items-query-ailifeassistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Natural-language summary derived from JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and LOSS_API_TOKEN; supports page, size, status, sort, and include_deleted parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
