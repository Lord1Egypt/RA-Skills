## Description:

A zero-dependency Bash health check for Linux, macOS, containers, and Kubernetes pods that reports system, user, tools, network, workspace, and optional PVC status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to check a workstation or project environment, confirm available tools and runtime details, identify container or Kubernetes context, and optionally monitor for a possible PVC remount.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious because it reports a serious command-execution flaw in the environment-check script; this does not establish malicious intent.

Mitigation: Review the script before installing, consider whether you trust the project content it may inspect, and avoid running it against untrusted projects.

## Reference(s):

- [hello-env on ClawHub](https://clawhub.ai/songhonglei/skills/hello-env)
- [Publisher profile](https://clawhub.ai/user/songhonglei)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain-text environment health report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detected environment details and statuses; optional config-file and PVC persistence checks depend on the supplied options and environment.]

## Skill Version(s):

1.0.3 (source: server-resolved release and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
