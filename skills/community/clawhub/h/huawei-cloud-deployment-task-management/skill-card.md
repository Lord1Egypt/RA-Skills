## Description:

Huawei Cloud CloudDeploy and CodeArts Deploy management, execution, and failure analysis using the KooCLI hcloud command-line client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to list, inspect, create, start, and delete Huawei Cloud CodeArts Deploy applications and deployment tasks, and to diagnose deployment failures or OBS artifact issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run read-only Huawei Cloud deployment queries automatically and can create, start, or delete deployment tasks after confirmation.

Mitigation: Use least-privilege IAM credentials, keep write permissions limited to operators who need them, and preserve the documented preview and explicit confirmation requirements for mutating actions.

Risk: The included quality reporting SDK may send runtime details, outputs, stack traces, or credential-backed telemetry outside the local environment.

Mitigation: Review or disable quality reporting before installation in environments where deployment details or telemetry must remain local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-deployment-task-management)
- [Huawei Cloud hcloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [hcloud KooCLI installation and authentication guide](references/cli-installation-guide.md)
- [IAM policies for Huawei Cloud CloudDeploy](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Test report](references/test-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured JSON-oriented results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query and analysis actions may run automatically; create, start, and delete actions require command preview and user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
