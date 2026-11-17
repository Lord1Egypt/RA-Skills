## Description:

Operate Alibaba Cloud ACK through an OOMOL-connected account to obtain a short-lived cluster kubeconfig.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cluster operators use the skill to request a short-lived kubeconfig for an Alibaba Cloud ACK cluster through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cluster login credentials are treated as ordinary data, and a returned kubeconfig contains sensitive access details.

Mitigation: Require an explicit request for a specific cluster, limit credential permissions and lifetime, and keep returned kubeconfigs out of chat and logs.

Risk: Setup can execute an unverified remote installer when the oo CLI is missing, and automatic skill synchronization may install unreviewed content.

Mitigation: Preinstall a verified CLI release and review or disable automatic skill synchronization.

## Reference(s):

- [Alibaba Cloud ACK](https://www.alibabacloud.com/product/kubernetes)
- [ACK DescribeClusterUserKubeconfig API documentation](https://www.alibabacloud.com/help/en/ack/ack-managed-and-ack-dedicated/developer-reference/api-cs-2015-12-15-describeclusteruserkubeconfig)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-aliyun-ack)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration]

**Output Format:** [Markdown guidance with Bash commands and JSON payloads; connector results may include kubeconfig data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A returned kubeconfig is short-lived and sensitive; keep it out of chat and logs.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
