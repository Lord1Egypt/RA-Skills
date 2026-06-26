## Description: <br>
Orchestrate an OpenClaw multi-agent pipeline to close Linux RISC-V gaps versus ARM/x86 (Linux tree + KVM lore), create and manage GitHub issues, generate design plans with Claude Code, implement/verify with Codex, and prepare upstream patch emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcxGGmu](https://clawhub.ai/user/zcxGGmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Kernel developers and maintainers use this skill to run a human-gated workflow for RISC-V Linux gap discovery, issue synchronization, design planning, implementation, verification, and upstream patch preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can affect local kernel code, GitHub issues, agent sessions, and patch preparation. <br>
Mitigation: Run it in a clean branch or disposable worktree, use least-privileged GitHub credentials, and review generated workflow values before execution. <br>
Risk: Patch emails or issue updates could be sent or published with incorrect recipients, content, or scope. <br>
Mitigation: Keep the human approval gates enabled and require explicit approval before issue updates or any email sending. <br>


## Reference(s): <br>
- [Human Gate Checklist](references/gate-checklist.md) <br>
- [Issue Template](references/issue-template.md) <br>
- [Workflow Template](references/workflow-template.yaml) <br>
- [KVM lore archive](https://yhbt.net/lore/kvm/) <br>
- [ClawHub skill page](https://clawhub.ai/zcxGGmu/linux-riscv-contribute) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, code] <br>
**Output Format:** [Markdown guidance with shell commands plus generated YAML, issue text, plans, test records, and patch email drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human approval at gap triage, implementation plan, and patch-send gates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
