## Description:

Infrastructure as Code security auditor for Terraform (.tf), CloudFormation (YAML/JSON), and Pulumi (TypeScript/Python). Detects 12 high-impact cloud misconfigurations including public S3 buckets, open SSH/RDP security groups, unencrypted storage, wildcard IAM policies, hardcoded credentials, missing deletion protection, public RDS, and unrestricted Lambda execution roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and security reviewers use this skill to scan Terraform, CloudFormation, and Pulumi infrastructure code for common cloud misconfigurations and to produce CI-friendly findings with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detected credential values may be printed to terminal output or CI logs.

Mitigation: Run the scanner only where logs are access-controlled, avoid scanning repositories with real secrets unless output is controlled, and redact findings before sharing logs.

Risk: CloudFormation, Pulumi, and Lambda role coverage is limited and may miss relevant issues.

Mitigation: Treat results as triage guidance and pair them with manual review or dedicated IaC security tooling before relying on the skill as a release gate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-iac-sec-audit)
- [Publisher Profile](https://clawhub.ai/user/phy041)
- [Homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, CI snippets, and finding summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity-filtered IaC security findings and remediation recommendations.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
