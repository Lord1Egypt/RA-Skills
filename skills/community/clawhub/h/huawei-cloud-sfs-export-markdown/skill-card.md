## Description:

Lists Huawei Cloud SFS file systems in a selected region and exports the results to a local Markdown file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators can export a regional Huawei Cloud SFS inventory for review, operations patrol, or handover. The skill writes a local Markdown report and only performs read-only cloud listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires quality telemetry software, and the data handling of remotely downloaded telemetry code is unresolved.

Mitigation: Before installation, require telemetry to be optional and review its implementation, collected fields, and destinations; disabling reports alone does not verify wrapper behavior.

Risk: The dependency installer weakens download security.

Mitigation: Install SDK dependencies with certificate verification enabled.

Risk: Cloud credentials and command overrides can affect access and execution scope.

Mitigation: Use read-only cloud credentials and leave command overrides unset unless they are trusted.

## Reference(s):

- [KooCLI / SDK Installation & Credential Guide](artifact/references/cli-installation-guide.md)
- [IAM Policies (least privilege, read-only)](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)
- [Data Flow Diagram](artifact/references/dataflow-diagram.md)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [ClawHub skill release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-sfs-export-markdown)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [Local Markdown table (.md) listing SFS file systems and their available metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is written locally; optional filters are applied client-side and recorded in the report.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
