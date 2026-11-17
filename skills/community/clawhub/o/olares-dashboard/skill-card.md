## Description:

Olares Dashboard helps agents query Olares Dashboard Overview and Applications data through olares-cli dashboard, including resource metrics, application rankings, JSON envelopes, and watch-mode output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olares](https://clawhub.ai/user/olares)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Olares dashboard metrics and application resource usage from an active olares-cli profile. It guides agents toward the correct dashboard commands, JSON output shapes, watch behavior, and empty-data semantics for CPU, memory, disk, pods, network, fan, GPU, ranking, and applications views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to query dashboard metrics through the active olares-cli profile, including admin-scoped views when --user targets another Olares ID.

Mitigation: Use the active profile intentionally, reserve --user for deliberate platform-admin visibility, and review profile scope before querying sensitive dashboard data.

Risk: Large result sets or live polling can add load or produce more output than needed.

Mitigation: Use output caps such as --head, --limit, --watch-iterations, and --watch-timeout, and respect the recommended polling cadence.

## Reference(s):

- [dashboard overview](references/olares-dashboard-overview.md)
- [dashboard --watch / windows / NDJSON contract](references/olares-dashboard-watch.md)
- [Olares Dashboard ClawHub skill page](https://clawhub.ai/olares/skills/olares-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON shape descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance centers on olares-cli dashboard output, including table, JSON, and NDJSON watch-mode behavior.]

## Skill Version(s):

4.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
