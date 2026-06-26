## Description: <br>
Helps agents query Huawei Cloud Config resource inventory, resource schemas, SQL-filtered resources, and built-in compliance rules for cloud asset auditing and compliance analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jupiter-19](https://clawhub.ai/user/jupiter-19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators, security reviewers, and developers use this skill to inspect Huawei Cloud Config inventory, understand resource schemas, run scoped SQL queries, and find built-in compliance rules for resource audit workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Huawei Cloud AK/SK credentials are required to query Config data. <br>
Mitigation: Use a dedicated credential with Config ReadOnlyAccess, store credentials in environment variables, and avoid printing or logging secret values. <br>
Risk: Resource inventory and compliance outputs can expose sensitive cloud architecture and security posture. <br>
Mitigation: Treat returned inventory as sensitive data and limit sharing, storage, and export of query results. <br>
Risk: Broad or unscoped SQL queries can return more inventory than intended. <br>
Mitigation: Prefer scoped queries with provider, resource type, region, and explicit fields; avoid SELECT * unless necessary. <br>
Risk: Untrusted SQL parameters may produce unintended query behavior. <br>
Mitigation: Review query strings before execution and do not pass untrusted values directly into query parameters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jupiter-19/huaweicloud-config-helper) <br>
- [Publisher profile](https://clawhub.ai/user/jupiter-19) <br>
- [Artifact README](artifact/SKILL.md) <br>
- [SQL query examples](artifact/scripts/sql-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return sensitive Huawei Cloud inventory details and compliance-rule metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
