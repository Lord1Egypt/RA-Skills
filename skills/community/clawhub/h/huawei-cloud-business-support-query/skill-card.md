## Description: <br>
Queries Huawei Cloud billing, pricing, balances, bills, coupons, orders, refunds, costs, resource usage, enterprise accounts, and supported pricing scenarios through read-only local Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and FinOps users can use this skill to inspect Huawei Cloud billing, pricing, order, coupon, resource usage, and account data from actual Huawei Cloud SDK/API responses. It is suited for read-only cost checks, price estimates, billing reviews, and consumption reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Huawei Cloud credentials and may expose billing, order, account, or infrastructure identifiers in query output. <br>
Mitigation: Use least-privilege, read-only credentials and treat all returned account, billing, and resource data as sensitive. <br>
Risk: The security scan reports unsafe TLS handling and local setup code that installs or runs dependencies. <br>
Mitigation: Review the scripts before installation, run them in an isolated environment, and disable or fix SSL verification bypasses before using real account data. <br>
Risk: Environment preparation may install dependencies from the network before queries can run. <br>
Mitigation: Allow automatic setup only in controlled environments where network dependency installation is acceptable. <br>


## Reference(s): <br>
- [BSS Python Script Usage Guide](references/bss/guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/huaweiclouddev/skills/huawei-cloud-business-support-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or tabular query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on Huawei Cloud SDK responses, configured credentials, and caller-supplied region or project scope.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
