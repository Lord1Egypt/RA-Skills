## Description:

Lists Huawei Cloud DCS instances through KooCLI or the Huawei SDK and exports the inventory as Markdown, a text table, or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators can use this skill to review Huawei Cloud DCS cache inventories by region and produce local reports for operations or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup includes a certificate-verification bypass.

Mitigation: Remove the bypass before setup and use vetted dependencies with normal HTTPS verification.

Risk: The optional quality helper may report telemetry.

Mitigation: Set SKILL_QUALITY_REPORT=0 and skip helper installation unless its telemetry behavior has been reviewed.

Risk: The generic test runner has safeguards that need review, and combining --name-equal with --tags has a known issue.

Mitigation: Restrict or avoid the generic test runner, and avoid combining --name-equal with --tags until fixed.

Risk: Cloud credentials with write permissions exceed the inventory task's needs.

Mitigation: Use only read-only cloud credentials.

## Reference(s):

- [Huawei Cloud CLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI Installation and Credential Guide](artifact/references/cli-installation-guide.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)
- [ClawHub Skill Page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-dcs-export-markdown)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Files]

**Output Format:** [Markdown report, text table, or JSON instance data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown reports are written to a local file; results can be filtered by region and instance attributes.]

## Skill Version(s):

1.0.9 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
