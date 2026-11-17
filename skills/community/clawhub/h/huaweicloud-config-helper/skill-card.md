## Description:

Helps agents use Huawei Cloud Config to query cloud resources, inspect resource schemas, run SQL-based resource inventory queries, and look up built-in compliance rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jupiter-19](https://clawhub.ai/user/jupiter-19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and security teams use this skill to audit Huawei Cloud assets, inspect Config resource schemas, generate SQL queries, and review built-in compliance rules for inventory, security, cost, and governance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Huawei Cloud credentials used with the skill could expose broader account access than the skill needs.

Mitigation: Use credentials limited to Config ReadOnlyAccess and run the skill only in a trusted environment.

Risk: Untrusted provider, region, resource type, or SQL inputs could cause unintended cloud inventory queries.

Mitigation: Validate query parameters and review generated SQL before running the bundled scripts.

Risk: Unpinned Huawei Cloud SDK dependency versions could change behavior over time.

Mitigation: Pin SDK dependency versions during installation and review updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jupiter-19/skills/huaweicloud-config-helper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, SQL examples, and JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run bundled Python scripts that return JSON-formatted Huawei Cloud Config results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
