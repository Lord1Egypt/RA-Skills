## Description:

Lists Huawei Cloud RDS instances in a selected region, supports filters and table, JSON, names-only, or Markdown output, and blocks write operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to review a Huawei Cloud region's RDS inventory, filter instances, and export reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags a remote installer and an environment-controlled command override that could run another program with cloud credentials; scanner analysis is partial.

Mitigation: Verify the installer through a trusted source before running it, and protect the environment variables that select the CLI executable and its arguments.

## Reference(s):

- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)
- [ClawHub release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-rds-list)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Terminal table, JSON array, names-only text, or Markdown report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only, region-scoped instance inventory with optional filters and pagination.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
