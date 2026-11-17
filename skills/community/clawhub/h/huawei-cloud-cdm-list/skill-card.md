## Description:

Lists Huawei Cloud CDM clusters and shows cluster details with read-only queries, filtering, and export options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and migration engineers use this skill to inventory Huawei Cloud CDM clusters, inspect their status and details, and export filtered reports for routine checks and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied setup path disables download security checks, and downloaded telemetry code has unverified data handling.

Mitigation: Install SDK dependencies in an isolated environment with certificate verification enabled; set SKILL_QUALITY_REPORT=0 and skip the optional quality-tool installation until its collection behavior and destination are documented.

Risk: Cloud credentials and exported reports can expose account access and infrastructure details.

Mitigation: Use credentials limited to CDM read access and store or share exported reports carefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-cdm-list)
- [Huawei Cloud KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM policies](references/iam-policies.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV]

**Output Format:** [Console table, JSON, Markdown table, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cluster list or single-cluster details; optional name and status filters and file export.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
