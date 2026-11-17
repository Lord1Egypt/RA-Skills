## Description:

Orchestrate an OpenClaw multi-agent pipeline to close Linux RISC-V gaps versus ARM/x86 (Linux tree + KVM lore), create and manage GitHub issues, generate design plans with Claude Code, implement/verify with Codex, and prepare upstream patch emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcxggmu](https://clawhub.ai/user/zcxggmu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and kernel engineers use this skill to coordinate human-reviewed Linux RISC-V contribution workflows, from gap discovery and GitHub issue tracking through design planning, implementation verification, and patch email preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow configuration includes external GitHub, agent, and model/provider destinations that could receive project details.

Mitigation: Before running the workflow, replace the repository, assignee, ACP agents, and model/provider values with trusted destinations and review workflow.yaml before issue sync or agent sessions.

Risk: Kernel issue creation, agent execution, and patch email preparation can publish or transmit work before it is ready if review gates are bypassed.

Mitigation: Keep the documented human gates in place, especially before creating issues, approving implementation plans, or sending patch email.

## Reference(s):

- [Human Gate Checklist](references/gate-checklist.md)
- [Issue Template](references/issue-template.md)
- [Workflow Template](references/workflow-template.yaml)
- [KVM lore archive](https://yhbt.net/lore/kvm/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration, issue templates, plans, verification notes, and patch email drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces auditable workflow artifacts under the configured OpenClaw workspace and pauses for documented human review gates before triage acceptance, plan approval, and patch email sending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
