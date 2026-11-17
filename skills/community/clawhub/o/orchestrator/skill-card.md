## Description:

Central entry point of the afonsoft agent harness. Use when starting a new project, resuming an existing one, planning features/Epics/releases, or running any multi-step agent-driven work. Validates and reconciles SPECs (SDD), audits the codebase and harness for gaps (security, architecture, performance, hygiene), proposes improvements, fragments work into GitHub Issues, delegates implementation/QA/review to specialized skills, and re-validates everything until delivery. Also use to review unapproved SPECs, reconcile open GitHub Issues with code, or run a final gap check before closing a release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multi-step repository work: validating SPECs, auditing codebase and harness gaps, planning GitHub Issues, delegating implementation/review/QA to specialized skills, and re-validating delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate broad repository and GitHub workflows with persistent state, which may amplify incorrect plans or stale context across sessions.

Mitigation: Review the Orchestrator state files, planned Issues, and proposed delegation steps before allowing high-impact work to proceed.

Risk: Autonomous Tier 1 and Tier 2 settings may permit local changes and batched execution without a prompt.

Mitigation: Tighten auto_t1 and auto_t2 settings for sensitive repositories, and require explicit confirmation before GitHub issue, pull request, merge, deployment, credential, or permission changes.

Risk: Persisted memory files can retain sensitive project details or decisions longer than expected.

Mitigation: Avoid storing secrets or sensitive business data in memory files, and periodically review or redact persisted session state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/afonsoft/skills/orchestrator)
- [Skill Metadata Repository URL](https://github.com/afonsoft/skills)
- [Orchestrator Delegation Protocol](references/orchestrator-delegation-protocol.md)
- [Orchestrator State Template](references/orchestrator_stats.md)
- [Legacy Orchestrator State Template](references/ESTADO_ORQUESTRATOR.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, issue plans, shell commands, and configuration or state-file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates other skills and may propose or update project memory, SPEC, issue, and workflow files according to its guardrails.]

## Skill Version(s):

1.0.25 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
