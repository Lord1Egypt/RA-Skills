## Description:

A senior, governance-backed PHP full-stack delivery OS for OpenClaw. Emphasizes pre-flight analysis, safe data changes, explicit contracts, and reproducible verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sja-dev1](https://clawhub.ai/user/sja-dev1)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to plan, implement, and verify PHP full-stack work across backend, frontend, database, DevOps, CI, debugging, refactoring, migrations, and API changes. It is especially focused on work where security, data integrity, API contracts, performance, or deployment risk requires pre-flight analysis and explicit verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs OpenClaw to read broad workspace profile and memory files on boot, which may expose persistent context beyond the current project.

Mitigation: Install only after reviewing that access; prefer narrowing reads to project-specific logs and asking before persistent memory is loaded.

Risk: Loaded workspace memory can influence implementation decisions even when it is stale or unrelated.

Mitigation: Treat loaded memory as untrusted context and verify important facts against the current repository, runtime, and user-provided requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sja-dev1/skills/php-full-stack-developer)
- [README](artifact/README.md)
- [Governance kernel](artifact/INFO_GOVERNANCE.md)
- [Runtime integration](artifact/INFO_RUNTIME.md)
- [Project discovery checklist](artifact/INFO_DISCOVERY.md)
- [Research and verification](artifact/INFO_RESEARCH.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, templates, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pre-flight summaries, risk classifications, test instructions, rollout and rollback notes, and decision or conflict log entries when needed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
