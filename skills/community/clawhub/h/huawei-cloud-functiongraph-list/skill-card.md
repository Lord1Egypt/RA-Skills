## Description:

Lists and filters Huawei Cloud FunctionGraph functions through KooCLI, with an SDK fallback and table, JSON, or names-only output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use the skill to inspect a Huawei Cloud FunctionGraph inventory for a selected account, project, and region. Its read-only listing and filters support routine operations checks and provide function details for follow-on work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security review says the required monitoring software's data handling is unspecified.

Mitigation: Prefer a release with optional telemetry. The documented reporting opt-out is SKILL_QUALITY_REPORT=0, though the wrapper requirement remains.

Risk: The release security review says the installer weakens download security.

Mitigation: Prefer authenticated, pinned downloads with normal certificate checks.

## Reference(s):

- [ClawHub release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-functiongraph-list)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation and credentials](artifact/references/cli-installation-guide.md)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Function inventory as an aligned table, JSON array, or names-only list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are sorted by function name; filters support function name, package, region, and page size.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
