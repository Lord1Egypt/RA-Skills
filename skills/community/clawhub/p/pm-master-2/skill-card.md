## Description:

Project and program management skill for technology teams that creates and governs artifacts such as charters, WBS, Gantt schedules, RAID logs, status reports, stage-gate reviews, EVM controls, DOCX exports, and SOW-driven expert dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slearnai](https://clawhub.ai/user/slearnai)

### License/Terms of Use:

MIT

## Use Case:

Project managers, program managers, delivery leads, and technical teams use this skill to create, update, and govern project artifacts across waterfall, agile, iteration, hybrid, and program workflows. It is most useful when the agent is expected to maintain a project source of truth, run quality gates, and produce delivery documents rather than provide general PM advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This skill is highly stateful and creates or updates project files.

Mitigation: Review generated artifacts and project.yaml changes before relying on them, keep workspace versioning or backups enabled, and run the documented consistency checks before delivery.

Risk: SOW parsing and project automation can change planned scope or work breakdown data.

Mitigation: Use preview or dry-run modes first, apply changes only after review, and keep the generated backup files for rollback.

Risk: The optional email capability can send formal external communications when enabled.

Mitigation: Keep email.enabled false unless needed, configure an administrator-controlled approver allowlist, require sponsor co-sign for external recipients, and use dry-run or draft review before approval.

Risk: Generated PM artifacts can contain sensitive project, customer, or stakeholder details.

Mitigation: Configure confidentiality.high_tokens and confidentiality.high_patterns for the installation, then run the pre-publish confidentiality scan before sharing outputs.

## Reference(s):

- [PM Master README](README.md)
- [Usage Guide](references/usage.md)
- [Project Schema](references/project-schema.md)
- [Lifecycle State Machine](references/lifecycle.md)
- [Program Management](references/program-management.md)
- [Templates Index](references/templates-index.md)
- [Orchestration Guide](references/orchestration.md)
- [PM Master on ClawHub](https://clawhub.ai/slearnai/skills/pm-master-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, YAML project state, DOCX exports, JSON reports, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates project files, can dispatch sub-agents, and can prepare external email only when configured and approved.]

## Skill Version(s):

2.2.17 (source: ClawHub release metadata, SKILL.md metadata, README, and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
