## Description:

MeshOps Control Plane is a distributed agent mesh for OpenClaw with ring-of-trust admission, CRDT-synced coordination across gateways, capability-contract routing, and governed task delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likesjx](https://clawhub.ai/user/likesjx)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw operators use this skill to coordinate work across multiple gateways, manage trust and delegation policy, bootstrap or repair the ansible plugin, and keep mesh operations auditable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task-driven authority over plugin installs, skill deployment, gateway restarts, and command execution can affect operator-controlled gateways.

Mitigation: Install only in an operator-controlled OpenClaw environment, keep high-risk gates disabled by default, and enable them only after caller identity is authenticated outside the task body.

Risk: Untrusted task files, path fields, or deployment archives could expand the skill's operational scope.

Mitigation: Accept task files only from trusted orchestration, strictly validate task and path fields, require SHA-256 archive checks, and harden archive extraction before enabling deployment.

Risk: Command execution can exceed intended scope if command allowlists are broad or stale.

Mitigation: Use exact command allowlists, keep command execution disabled unless needed, and review generated stdout, stderr, and status artifacts.

## Reference(s):

- [MeshOps Control Plane ClawHub Page](https://clawhub.ai/likesjx/skills/meshops-control-plane)
- [OpenClaw](https://openclaw.ai/)
- [openclaw-plugin-ansible](https://github.com/likesjx/openclaw-plugin-ansible)
- [README](README.md)
- [Operator Runbook](docs/operator-runbook.md)
- [Runbook](docs/runbook.md)
- [Plugin Capability Inventory](docs/plugin-capabilities-actual-v2026-03-03.md)
- [Ansible Coordination Mesh Specification](docs/ansible-mesh-spec.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, json]

**Output Format:** [Markdown guidance with inline shell commands plus JSON and text artifacts from operational actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw, the ansible plugin, jq, curl, tar, a SHA-256 tool, timeout, git, and operator-controlled environment gates for high-risk actions.]

## Skill Version(s):

0.1.7 (source: server release metadata and artifact metadata.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
