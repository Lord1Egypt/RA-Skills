## Description:

Manages Huawei Cloud DDS and DCS instances with query, analysis, and supported lifecycle operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and database or cache administrators use this skill to inspect DDS and DCS deployments, review deployment and security details, and manage supported instance operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic quality reporting can send unrelated private conversation content and cloud-command output to an external service.

Mitigation: Set SKILL_QUALITY_REPORT=0 before use. Enable reporting only after reviewing its collection and destination; safer reporting requires explicit consent, invocation-bound collection, redaction, and restricted HTTPS destinations.

Risk: Cloud management actions can create billable resources, interrupt service, or permanently delete instance data.

Mitigation: Prefer narrowly scoped, read-only credentials for inspection. Review shell startup changes and avoid the combined wildcard administrator policy. Confirm exact targets and parameters before mutations, and double-confirm destructive actions.

Risk: The downloaded hcloud binary and external service retention behavior are unverified in the supplied security evidence.

Mitigation: Review the CLI source and download integrity where possible, and establish acceptable data-retention terms before enabling external reporting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-dds-dcs-instance-management)
- [CLI installation and authentication](artifact/references/cli-installation-guide.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Unsupported operations and alternatives](artifact/references/out-of-scope.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Python code, Configuration guidance]

**Output Format:** [Markdown with shell command examples and Python SDK snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers documented Huawei Cloud DDS and DCS operations; unsupported services and actions are identified as out of scope.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
