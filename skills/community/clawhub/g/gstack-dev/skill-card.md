## Description:

Gstack AI虚拟工程团队 turns a single AI assistant into a role-based engineering workflow for product thinking, planning, implementation, review, testing, release, and retrospectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangbotaochn](https://clawhub.ai/user/wangbotaochn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure feature work, bug fixes, refactors, technical reviews, QA, deployment, and sprint retrospectives through specialized AI roles and stage-specific checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can authorize broad automatic edits, testing, and release actions across a repository.

Mitigation: Install it only in repositories where agent edits and release preparation are acceptable, and require user confirmation before deployment, production changes, destructive operations, or force pushes.

Risk: The cross-check workflow may send project plans or code to another model provider.

Mitigation: Disable external cross-model review unless the provider, model, and content being shared have been explicitly approved.

Risk: The reflection workflow can persist project lessons or experience entries beyond the current task.

Mitigation: Do not allow automatic writes to global or shared memory; review and approve any retained knowledge before saving it.

Risk: The testing and shipping phases reference production-like validation and deployment steps.

Mitigation: Keep production testing read-only by default and use documented rollback, health-check, and canary controls for any approved release work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangbotaochn/skills/gstack-dev)
- [Garry Tan's gstack](https://github.com/garrytan/gstack)
- [ClawHub publisher profile](https://clawhub.ai/user/wangbotaochn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, implementation guidance, code changes, test plans, release checklists, and shell commands when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate multi-stage engineering workflows and produce phase-specific reports for downstream review.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
