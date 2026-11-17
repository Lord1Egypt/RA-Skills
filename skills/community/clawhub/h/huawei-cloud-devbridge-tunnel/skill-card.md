## Description:

Helps developers create and manage Huawei Cloud DevBridge tunnels to share local development services with remote devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and authenticate the DevBridge CLI, create and manage temporary tunnels and ports, and connect remote devices to local development services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can install or upgrade the CLI and start long-running tunnel processes without asking first.

Mitigation: Require explicit approval for installation, upgrades, and background host or connect sessions; stop sessions after use.

Risk: Tunnel hosting can expose local services or sensitive development endpoints remotely.

Mitigation: Confirm the service, port, access policy, and duration before hosting; deny anonymous access unless explicitly requested.

Risk: Credential handling may expose API Keys, especially when initialization sources wildcard files in shared sandbox environments.

Mitigation: Use an isolated workspace, keep credentials out of logs, and change initialization to read only the intended credential value as data rather than sourcing wildcard files.

Risk: Delete commands can remove tunnels or ports, including other users' resources in a shared workspace.

Mitigation: List affected resources and obtain explicit confirmation before any delete operation, especially delete-all.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-devbridge-tunnel)
- [DevBridge API Key management](https://devstation.connect.huaweicloud.com/space/devbridge/apikey)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [CLI command reference](artifact/references/cli-command-reference.md)
- [API Key and access guidance](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Tunnel status and URLs]

**Output Format:** [Markdown with shell commands and tunnel details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Development and temporary sharing only; not a production service.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
