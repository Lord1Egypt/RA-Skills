## Description:

Query Huawei Cloud BSS vouchers and filter them by enterprise project, status, name, ID, type, and expiry, with per-project usage summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Huawei Cloud account administrators and finance teams can inventory BSS vouchers, identify vouchers by enterprise project or expiry, and review usage rates for reconciliation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically reports session information to a separate service without clearly disclosing this behavior; service retention and CLI installer contents are unverified.

Mitigation: Prefer a version with telemetry removed or explicitly opt-in and limited to the current invocation. SKILL_QUALITY_DISABLE=1 blocks transmission but does not prevent earlier configuration and session-file reads; use read-only cloud permissions and verify the CLI installer separately.

## Reference(s):

- [Least-privilege IAM policies](references/iam-policies.md)
- [KooCLI installation and authentication](references/cli-installation-guide.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Tables, Analysis]

**Output Format:** [Human-readable voucher table, JSON array, names-only list, or per-project usage summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports paging and filters; project attribution uses linked customer orders and can omit vouchers without attributable orders.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
