## Description: <br>
Openclaw Skill Ansible teaches agents to operate a distributed OpenClaw mesh with ring-of-trust admission, CRDT-synced coordination, capability-contract routing, and governed task delegation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likesjx](https://clawhub.ai/user/likesjx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw operators and developers use this skill to coordinate work across multiple gateways, maintain durable mesh state, publish capability contracts, and run gated lifecycle operations with human-visible status updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate broad mesh operations, including deployment and command actions. <br>
Mitigation: Install it only in controlled operator environments, keep high-risk gates disabled by default, and restrict allowed callers to authenticated operators. <br>
Risk: Downloaded skill artifacts or host command execution can affect the gateway host. <br>
Mitigation: Review artifact sources before use, require explicit approval for host execution, and sandbox downloaded artifact scripts separately before enabling deployment actions. <br>
Risk: Capability publishing and mesh trust flows can route work across gateways if governance settings are too permissive. <br>
Mitigation: Require approval artifacts for high-risk capability publishes, keep caller gates configured, and enforce trusted publisher signatures where available. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/likesjx/openclaw-skill-ansible) <br>
- [OpenClaw Skill README](README.md) <br>
- [MeshOps Coordination Skill](SKILL.md) <br>
- [Operator Runbook](docs/runbook.md) <br>
- [Plugin Capability Inventory](docs/plugin-capabilities-actual-v2026-03-03.md) <br>
- [OpenClaw Ansible Plugin](https://github.com/likesjx/openclaw-plugin-ansible) <br>
- [OpenClaw](https://openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON task/action outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke gated OpenClaw mesh actions that write logs and JSON results under the configured artifact root.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata and artifact metadata.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
