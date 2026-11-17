## Description:

Queries Huawei Cloud monitoring and enterprise project resources (CES/EPS), including alarm rules, alarm histories, alarm templates, dashboards, notification masks, resource groups, one-click alarms, and enterprise projects, without write operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Huawei Cloud CES monitoring data and EPS enterprise project information, including alarms, dashboards, resource groups, quotas, bound resources, and migration records. It is intended for read-only inventory, verification, troubleshooting, and parameter discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Huawei Cloud traffic and credentials could be exposed if setup or network handling is used without fixing the reported TLS verification risk.

Mitigation: Use least-privileged Huawei Cloud credentials, avoid sensitive machines, and do not run setup until TLS verification issues are fixed.

Risk: The setup path can execute mutable remote bootstrap code in a fallback path.

Mitigation: Remove or replace the remote get-pip.py bootstrap behavior before installation, or review and pin the setup process in a controlled environment.

Risk: The skill can return broad cloud inventory or monitoring data when queries are not scoped.

Mitigation: Scope queries by region, project, enterprise project, resource name, ID, status, or tag, and avoid exposing credential environment variable values in outputs.

## Reference(s):

- [Huawei Cloud Monitoring Query on ClawHub](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-monitoring-query)
- [CES Python Script Usage Guide](references/ces/guide.md)
- [Enterprise Project EPS Python Script Usage Guide](references/eps/guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON query results from local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Huawei Cloud query workflow; large result sets should be narrowed or cached.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
