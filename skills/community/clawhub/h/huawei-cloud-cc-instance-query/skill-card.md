## Description:

Queries Huawei Cloud Cloud Connect resources through the hcloud CLI for read-only inspection of cloud connections, bandwidth packages, inter-region bandwidths, network instances, routes, and cross-account authorisations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud and network engineers use this skill to inspect Huawei Cloud Cloud Connect topology, bandwidth allocation, routing, and cross-account authorisation relationships without performing write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials can expose Huawei Cloud account data if overprivileged or mishandled.

Mitigation: Use least-privilege CC ReadOnlyAccess credentials and avoid sharing AK/SK values in prompts, logs, or generated examples.

Risk: The hcloud CLI may use a default domain_id when one is not supplied, which can query the wrong account.

Mitigation: Specify --domain_id and --cli-region explicitly for each Cloud Connect query and verify the account ID before running commands.

Risk: Installing the CLI through a downloaded shell script introduces installer-source risk.

Mitigation: Verify the Huawei Cloud CLI installer source before running the downloaded script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cc-instance-query)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [API Reference](references/api-reference.md)
- [Verification Method](references/verification-method.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Huawei Cloud KooCLI Installer](https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/hcloud_install.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with hcloud CLI commands and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Cloud Connect query guidance; command results are returned by the Huawei Cloud CLI as JSON or formatted CLI output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
