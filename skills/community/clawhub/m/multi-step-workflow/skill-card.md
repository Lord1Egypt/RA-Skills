## Description:

Professional SOP with Machine-Gated Planning, Native-CLI Config, and Audit-Hardened Private Sandbox Storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chyern](https://clawhub.ai/user/chyern)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to apply a structured workflow for complex workspace tasks, including planning, approval gating, task tracking, autonomous execution, validation, and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional snapshots may store raw task context, and the clear command may leave saved snapshot contents available.

Mitigation: Keep useSnapshots disabled unless task recovery is needed, avoid placing secrets in snapshots, and manually delete sensitive snapshot files until the clear behavior is fixed.

Risk: The skill runs local Node.js scripts and writes approval and task state to project-specific temporary storage.

Mitigation: Review the bundled scripts before deployment, use the skill only in trusted workspaces, and account for local temporary storage in endpoint security controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chyern/skills/multi-step-workflow)
- [ClawHub publisher profile](https://clawhub.ai/user/chyern)
- [Project homepage from ClawHub metadata](https://github.com/chyern/Agent-Skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON approval, task-tracking, and optional context-snapshot state through bundled Node.js scripts.]

## Skill Version(s):

4.4.5 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
