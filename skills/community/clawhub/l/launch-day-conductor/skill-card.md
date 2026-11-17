## Description:

Launch Day Conductor helps agents run a launch-day war room by checking readiness and date prerequisites, creating an owner-assigned hour-blocked runbook, forcing CONTINUE-or-ROLLBACK decisions after irreversible actions, and organizing incident response plus end-of-day consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Launch, marketing, and product operators use this skill to coordinate the execution day for a release. It turns validated readiness inputs, owner rosters, channel plans, and rollback criteria into a launch-day runbook, observation-window decisions, incident handling, and handoff notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads launch readiness records, registry state, rollback thresholds, and launch metrics that may affect launch decisions.

Mitigation: Confirm installation is appropriate for those records before use, and keep rollback execution plus saved memory updates under explicit owner approval.

Risk: Telemetry exports, dashboard screenshots, and community threads may contain untrusted or misleading content.

Mitigation: Treat pasted telemetry as input evidence only, require pre-declared kill criteria for decisions, and avoid following instructions embedded in metrics or comments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/launch-day-conductor)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown runbook, verdict log, incident ladder, consolidation summary, and handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires launch readiness records, registry date or stage evidence, owner roster, channel plan, and pre-declared rollback criteria before irreversible launch actions.]

## Skill Version(s):

19.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
