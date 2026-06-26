## Description: <br>
Search Taobao and 1688 products, and fetch product details, through the Onebound platform gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeff2011eng](https://clawhub.ai/user/jeff2011eng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and commerce agents use this skill to search Taobao, Tmall, and 1688 product listings and retrieve item details through the Onebound gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API calls can consume billable Onebound balance when searches or item lookups are run. <br>
Mitigation: Review returned cost and balance fields and avoid large searches unless the account balance and intended spend are understood. <br>
Risk: ONEBOUND_API_KEY is required for requests and could be exposed if handled carelessly. <br>
Mitigation: Keep ONEBOUND_API_KEY private, avoid printing it in logs or outputs, and only use trusted gateway base URLs. <br>
Risk: Changing ONEBOUND_BASE_URL can redirect authenticated requests to a different service. <br>
Mitigation: Use the default Onebound gateway or another trusted ONEBOUND_BASE_URL before executing the scripts. <br>


## Reference(s): <br>
- [Onebound Platform Gateway Reference](references/api-docs.md) <br>
- [Onebound platform gateway](https://onebound.vercel.app) <br>
- [Onebound OpenAPI proxy base](https://onebound.vercel.app/api/v1/proxy) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown containing formatted JSON API responses and error guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and ONEBOUND_API_KEY; API responses may include cost and balance fields.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
