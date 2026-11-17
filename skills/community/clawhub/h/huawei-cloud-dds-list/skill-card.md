## Description:

Lists Huawei Cloud DDS instances for a selected region or project and returns names, a table, or JSON with filtering and pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use the skill to inspect Huawei Cloud DDS instances for inventory checks and as a read-only lookup before other DDS tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scanners flagged package installation and command-override controls as broader than the stated read-only DDS listing purpose; analysis coverage was incomplete.

Mitigation: Review the installation scripts and command resolution, address the flagged concerns, and rerun security scans before installing.

## Reference(s):

- [KooCLI installation and credential guide](references/cli-installation-guide.md)
- [Verification method](references/verification-method.md)
- [Least-privilege IAM policies](references/iam-policies.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text instance names or table, or a JSON array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Names list by default; optional fixed-column table or raw JSON, with filters and automatic pagination.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
