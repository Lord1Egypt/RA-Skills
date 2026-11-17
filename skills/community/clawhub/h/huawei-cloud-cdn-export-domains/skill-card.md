## Description:

Queries Huawei Cloud CDN accelerated domains and exports the results locally as CSV, Markdown, or JSON, with an optional table view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and operations engineers use this skill to inventory a tenant's Huawei Cloud CDN accelerated domains and save the results for reporting or handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags weakened download security in environment setup.

Mitigation: Install SDK dependencies separately with certificate verification enabled, preferably in an isolated environment.

Risk: The quality reporting executable is separately downloaded and its behavior is unverified; telemetry behavior is insufficiently explained.

Mitigation: Set SKILL_QUALITY_REPORT=0 and skip quality-tool installation until the executable and reporting behavior are reviewed.

Risk: The generic live test runner exceeds the documented read-only scope.

Mitigation: Use the documented offline tests instead of the generic live runner.

Risk: The SDK fallback ignores exact-match filtering.

Mitigation: Check exported domains before sharing the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-cdn-export-domains)
- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [IAM policies](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Files, CSV, Markdown, JSON, Text]

**Output Format:** [CSV, Markdown, or JSON export files; optionally an aligned table on standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports server-side filters and region selection; file exports use a local path.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
