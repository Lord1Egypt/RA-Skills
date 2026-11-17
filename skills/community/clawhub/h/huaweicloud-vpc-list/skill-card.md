## Description:

Lists VPCs in a configured Huawei Cloud region and returns a concise inventory of VPC names and IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to inventory VPC resources in one Huawei Cloud region for asset review, operations checks, or automation preflight steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or untrusted region value could cause signed credential metadata to be sent to a non-Huawei host.

Mitigation: Use a fixed Huawei Cloud region allowlist or validate the final request host before running the skill with real credentials.

Risk: The skill requires Huawei Cloud AK/SK credentials in local configuration.

Mitigation: Use a dedicated Huawei Cloud key with only the documented read-only VPC and IAM permissions, keep the config file out of shared storage, and rotate the key regularly.

## Reference(s):

- [IAM permission requirements](artifact/iam-policies.md)
- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/huaweicloud-vpc-list)
- [Publisher profile](https://clawhub.ai/user/yangaiwu)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single-region VPC name-and-ID list; returns exit code 0 for success or no VPCs and exit code 1 for configuration, authentication, network, or API errors.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
