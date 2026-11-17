## Description:

Checks Redis cluster metadata files (nodes-*.conf) for integrity, detecting 7 categories of metadata issues that cause Redis instance startup failures, connection anomalies, and fault alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MRS Redis operators use the skill to statically check supplied nodes-*.conf files for metadata issues that can cause startup failures, connection anomalies, or fault alerts. It returns a check report and manual repair guidance when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes automatic quality reporting and installers for a CLI whose behavior cannot be verified from the supplied evidence.

Mitigation: Prefer a version without the quality CLI and reporting command. If retained, require explicit telemetry consent, documented transmitted fields, and authenticated, pinned downloads.

Risk: Incorrect Redis metadata repairs can affect instance startup and cluster health.

Mitigation: Keep repairs manual and retain recovery backups before applying changes.

## Reference(s):

- [Skill release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-mrs-redis-meta-check)
- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [Huawei Cloud KooCLI installation documentation](https://support.huaweicloud.com/cli/index.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Plain-text check report with manual repair guidance when checks fail]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static analysis of supplied nodes-*.conf files; no cluster connection or file modification.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
