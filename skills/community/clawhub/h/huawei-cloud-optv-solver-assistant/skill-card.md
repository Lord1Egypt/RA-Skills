## Description:

Guides an agent through Huawei Cloud OptVerse demand analysis, mathematical modeling, data validation, solving, and asset publishing for operations research problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations researchers use this skill to turn optimization requirements and business data into validated OptVerse models, solver results, reports, and published assets.

### Deployment Geography for Use:

China (OptVerse operations are documented for the cn-east-3 region)

## Known Risks and Mitigations:

Risk: Insecure connections, unsafe download paths, unreliable approval checks, or token storage can put credentials and local files at risk.

Mitigation: Wait for fixes to certificate verification, download-path confinement, approval checks, and token storage before supplying real credentials.

Risk: Selected requirement documents and spreadsheets are sent to Huawei Cloud and may contain sensitive business data.

Mitigation: Use approved data, apply narrowly scoped cloud permissions, and review the CLI privacy agreement before uploading files.

Risk: The optional deployment workflow can create a running cloud service.

Mitigation: Ask the user to explicitly choose whether to deploy before creating the service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-optv-solver-assistant)
- [API Reference](artifact/references/api-reference.md)
- [Workflow Design](artifact/references/workflow-design.md)
- [Best Practices & Notes](artifact/references/best-practices.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Analysis, Code, Files, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown, Python, JSON, spreadsheet templates, solver artifacts, and cloud workflow commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce requirement analyses, model code and data templates, validated data, solver outputs, and reports; publishing and deployment involve cloud operations.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
