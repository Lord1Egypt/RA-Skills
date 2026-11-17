## Description:

Queries Huawei Cloud CCI resources through KooCLI hcloud using read-only list, read, and get operations for namespaces, Pods, workloads, services, networks, and related Kubernetes resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inspect Huawei Cloud CCI namespaces, Pods, workloads, services, networks, and related resources during routine checks, troubleshooting, and inventory without making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can configure and persist Huawei Cloud AK/SK credentials in the hcloud default profile.

Mitigation: Use a least-privilege test IAM user, avoid production AK/SK, and remove or isolate the hcloud default profile after use.

Risk: Secret query commands can expose Kubernetes Secret data in command output.

Mitigation: Do not run Secret queries unless explicitly needed, and route any output through the same handling controls used for sensitive cloud data.

Risk: The installation guide recommends executing a remotely downloaded hcloud installer without pinning or verification.

Mitigation: Download the installer to a temporary path, verify the source and integrity, and use a pinned installer version before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yangaiwu/skills/huawei-cloud-cci-query)
- [CCI hcloud Command Reference](artifact/cci-cli-reference.md)
- [IAM Permission Policy](artifact/iam-policies.md)
- [hcloud CLI Installation and Authentication Guide](artifact/cli-installation-guide.md)
- [Verification Method](artifact/verification-method.md)
- [Dataflow Diagram](artifact/dataflow-diagram.md)
- [Huawei Cloud KooCLI Installation Documentation](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud Regions and Endpoints](https://developer.huaweicloud.com/intl/en-us/endpoints)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON or table command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires hcloud/KooCLI, Python 3.8+, Huawei Cloud AK/SK environment variables, and an explicit region.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
