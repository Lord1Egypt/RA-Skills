## Description:

Queries and analyzes Huawei Cloud CTS audit traces, reviews retention, and manages trackers and notifications through the hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to inspect CTS audit activity, assess trace retention, and manage trackers or notifications. It returns structured query results and summarizes findings for the requested region and account scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic quality reporting can send audit output and may include unrelated private conversation content without asking first.

Mitigation: Set SKILL_QUALITY_REPORT=0 before invocation to disable session collection and reporting; use opt-in, redacted reporting only after reviewing what will be sent.

Risk: The helper CLI installer writes files under ~/.local/bin and may update ~/.bashrc or ~/.profile.

Mitigation: Review the installer and use an isolated environment. Disabling reporting does not prevent installer changes.

Risk: Creating or deleting CTS resources changes cloud audit configuration.

Mitigation: Use read-only cloud permissions for queries and require explicit approval after previewing each write command.

## Reference(s):

- [CLI installation and authentication guide](references/cli-installation-guide.md)
- [CTS IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Data flow diagrams](references/dataflow-diagram.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance, Shell commands]

**Output Format:** [Structured JSON results with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped by region, project or account, time range, and optional trace filters.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
