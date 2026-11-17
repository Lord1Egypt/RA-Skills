## Description:

Lists a Huawei Cloud OBS account's buckets and returns a local PDF report, text table, or JSON inventory using read-only bucket listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers can use the skill to review an account's OBS bucket inventory and create a local PDF report, or request table or JSON output for further review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and remote installer contents have not been verified.

Mitigation: Install reviewed dependencies in an isolated environment with certificate verification enabled, and use Huawei's download and checksum guidance.

Risk: Extra-command environment overrides or SDK fallback may not enforce endpoint or count restrictions.

Mitigation: Clear the extra-command environment overrides and do not rely on SDK fallback to enforce endpoint or count restrictions.

Risk: Cloud credentials could be exposed or granted broader access than bucket listing requires.

Mitigation: Use bucket-list-only credentials and keep secrets out of chat.

## Reference(s):

- [CLI installation and credential guide](references/cli-installation-guide.md)
- [Least-privilege IAM policy](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Huawei Cloud KooCLI download and checksum guidance](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Files, Text, JSON]

**Output Format:** [PDF report, aligned text table, or JSON bucket records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists buckets only; PDF reports are saved locally and can include an optional total-count summary.]

## Skill Version(s):

1.0.11 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
