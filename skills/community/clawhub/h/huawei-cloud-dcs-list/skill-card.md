## Description:

Lists Huawei Cloud DCS Redis and Memcached instances in a selected region and returns a name list, table, JSON, or Markdown with optional filtering and paging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this read-only skill to inspect Huawei Cloud DCS inventory in a region, apply server-side filters, and export results for review or downstream tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this skill suspicious: scanners report that exact-name mode can drop a tag restriction and environment settings may select an arbitrary executable; inspection was partial.

Mitigation: Follow Skillspector guidance and do not install while the suspicious verdict and incomplete inspection remain unresolved; have the reported behavior reviewed first.

## Reference(s):

- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [API Verification Method](references/verification-method.md)
- [Least-Privilege IAM Policies](references/iam-policies.md)
- [KooCLI Installation and Credential Guide](references/cli-installation-guide.md)
- [ClawHub Skill Release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-dcs-list)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Instance-name list, text table, JSON array, or GitHub-flavored Markdown table; optional Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional filters and stable client-side sorting; automatic pagination]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
