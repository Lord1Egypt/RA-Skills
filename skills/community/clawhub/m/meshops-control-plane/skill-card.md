## Description: <br>
Distributed agent mesh for OpenClaw: ring-of-trust admission, CRDT-synced coordination across gateways, capability-contract routing, and governed task delegation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likesjx](https://clawhub.ai/user/likesjx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw operators use this skill to coordinate distributed agent systems across gateways with explicit trust controls, durable routing, and auditable delegation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact deployment and command actions can alter an OpenClaw environment when enabled. <br>
Mitigation: Keep high-risk gates disabled by default and enable them only for trusted callers with an explicit operational need. <br>
Risk: Downloaded deployment artifacts and smoke tests may execute code on the target host. <br>
Mitigation: Restrict deploy sources, require expected SHA-256 hashes, and run downloaded artifact smoke tests only in a sandboxed or otherwise trusted environment. <br>
Risk: Command execution is sensitive to task creation controls and environment configuration. <br>
Mitigation: Use a strict command allowlist, tightly control operator accounts, and review environment variables before installation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/likesjx/meshops-control-plane) <br>
- [OpenClaw](https://openclaw.ai/) <br>
- [OpenClaw Ansible plugin](https://github.com/likesjx/openclaw-plugin-ansible) <br>
- [OpenClaw Ansible skill repository](https://github.com/likesjx/openclaw-skill-ansible) <br>
- [Operator runbook](docs/operator-runbook.md) <br>
- [Ansible coordination mesh specification](docs/ansible-mesh-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON task artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates OpenClaw mesh operations and emits task/action results through configured artifact files.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata and artifact metadata.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
