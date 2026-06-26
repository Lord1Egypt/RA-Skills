## Description: <br>
Get Shit Done - Full project planning and execution workflow. Handles project initialization with deep context gathering, automated research, roadmap creation, phase planning, and execution with verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oleg-schmidt](https://clawhub.ai/user/oleg-schmidt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to move software projects from an initial idea through context gathering, domain research, requirements, roadmaps, phase plans, implementation, debugging, and verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent repository and environment changes, including code edits, shell commands, git commits, tags, and selected destructive operations. <br>
Mitigation: Run it in a sandboxed workspace or disposable branch, keep interactive gates enabled, and review diffs before pushing or tagging. <br>
Risk: Some workflows may request secrets or service credentials so automation can configure external integrations. <br>
Mitigation: Avoid pasting long-lived secrets into chat, prefer scoped or temporary credentials, and require explicit approval before global installs, deployments, or external service changes. <br>
Risk: Automated planning and verification can still produce incorrect tasks, incomplete implementation checks, or misleading project state. <br>
Mitigation: Review generated plans and verification reports, run project tests independently, and require human approval at decision and destructive-action checkpoints. <br>


## Reference(s): <br>
- [Questioning guide](references/questioning.md) <br>
- [Checkpoint reference](references/checkpoints.md) <br>
- [Git integration](references/git-integration.md) <br>
- [Verification patterns](references/verification-patterns.md) <br>
- [Planning configuration](references/planning-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown project artifacts, implementation guidance, shell commands, code changes, and structured planning files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .planning Markdown and JSON files, run tools, edit code, and commit changes when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
