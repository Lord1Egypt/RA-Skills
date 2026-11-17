## Description:

Lists Huawei Cloud Elastic Load Balance instances in a selected region through KooCLI, with an official SDK fallback and table, JSON, or Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect Huawei Cloud load balancers by region, filter inventory, and retrieve IDs or names for follow-up work. Its queries are read-only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and command overrides need review before use.

Mitigation: Have the installer corrected before use, retain certificate verification, pin and verify dependencies in an isolated environment, obtain KooCLI through Huawei's documented downloads, and clear both command override variables.

Risk: Cloud credentials or generated Markdown output may be used or written in an unintended scope or location.

Mitigation: Use project-scoped read-only credentials and choose a trusted Markdown output path or disable Markdown output.

## Reference(s):

- [KooCLI Installation & Credential Guide](references/cli-installation-guide.md)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-Privilege IAM Policy](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [ClawHub Skill Page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-elb-list)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Text table, JSON array, or Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region and server-side filters; Markdown output can be redirected or disabled.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
