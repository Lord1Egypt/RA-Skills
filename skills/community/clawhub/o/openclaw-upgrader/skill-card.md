## Description: <br>
Upgrade OpenClaw to a specific version or latest using a cross-platform, Codex-supervised flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gejiliang](https://clawhub.ai/user/gejiliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to upgrade a same-host OpenClaw installation while delegating package update, service recovery, endpoint verification, and structured result reporting to a local coding agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad local OpenClaw upgrade, repair, restart, and verification actions on the current machine. <br>
Mitigation: Use it only when you intend same-host OpenClaw upgrade authority, and review the selected agent, target version, and generated files under ~/.openclaw before running the delegated workflow. <br>
Risk: Delegation hooks can affect how the local upgrade agent is invoked. <br>
Mitigation: Review any OPENCLAW_UPGRADER_DELEGATE_CMD setting before use and confirm it invokes the intended local Codex or Claude session. <br>


## Reference(s): <br>
- [OpenClaw Upgrader on ClawHub](https://clawhub.ai/gejiliang/openclaw-upgrader) <br>
- [OpenClaw Upgrader Review Checklist](references/review-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result/context files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces host upgrade context and structured upgrade result files for delegated agents.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
