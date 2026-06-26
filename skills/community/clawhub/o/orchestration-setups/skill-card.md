## Description: <br>
Hybrid orchestration skill where OpenClaw stays the control plane and ACP Claude Code is the default execution backend for coding work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkobject](https://clawhub.ai/user/jkobject) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multi-step coding, review, research, and recovery workflows while keeping OpenClaw as the control plane and ACP Claude Code or Codex workers as execution backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate persistent coding workers and may require API-key-backed gateway credentials. <br>
Mitigation: Scope worker prompts and artifact paths narrowly, protect and rotate gateway API keys, and avoid placing secrets in handoffs or run-state files. <br>
Risk: Unattended ACP worker execution depends on permission policy and referenced helper behavior. <br>
Mitigation: Review ACPX permission settings and inspect any referenced helper scripts before running workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jkobject/orchestration-setups) <br>
- [Skill entrypoint](artifact/SKILL.md) <br>
- [Reproducing the Setup](artifact/docs/reproduction.md) <br>
- [Detailed Setup Matrix](artifact/docs/setup-matrix.md) <br>
- [Orchestration Control Plane V1](artifact/docs/design/control-plane-v1.md) <br>
- [Test Results](artifact/docs/test-results.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with YAML workflow and agent configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes handoff templates, workflow definitions, setup notes, and smoke-test guidance for OpenClaw and ACP worker orchestration.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
