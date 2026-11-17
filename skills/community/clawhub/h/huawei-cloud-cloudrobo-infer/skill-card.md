## Description:

Manage CloudRobo inference services by deploying models, checking deployment status and logs, and starting, stopping, updating, or deleting services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy a model as a CloudRobo inference service and manage its lifecycle, status, and logs within a workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment says the CLI installation guide was only partly inspected.

Mitigation: Review the installation guide before installing or upgrading the CLI.

Risk: The security assessment says the reported asset-file retrieval was not fully explained.

Mitigation: Inspect asset retrieval requests and confirm each downloaded file is needed for the selected deployment before using it.

## Reference(s):

- [CLI Installation Guide](references/cli-installation-guide.md)
- [Authentication and Access Control](references/iam-policies.md)
- [Service Configuration Reference](references/service-config-catalog.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, deployment guidance, service status and log summaries]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and deployment parameters are resolved from the user's workspace, model, and available compute pools.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
