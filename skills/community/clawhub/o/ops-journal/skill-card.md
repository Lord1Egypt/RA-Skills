## Description:

Automates logging of deployments, incidents, changes, and decisions into a searchable ops journal with incident timelines and postmortem generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to maintain a structured local record of deployments, incidents, maintenance, configuration changes, security events, and operational decisions. It supports incident tracking, timeline reconstruction, period summaries, statistics, and report exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational notes may contain sensitive incident details, infrastructure context, or credentials if users enter them.

Mitigation: Avoid logging secrets, restrict access to the local journal directory, and review entries before sharing or exporting reports.

Risk: Exports to Markdown, JSON, or CSV can expose accumulated operational history outside the local journal store.

Mitigation: Export only the required time window, store exported files in controlled locations, and treat CSV or report files as sensitive operational records.

Risk: Writing reports to user-specified paths may overwrite or place files where unintended readers can access them.

Mitigation: Check output paths before export or timeline generation and avoid shared or world-readable directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariusfit/skills/ops-journal)
- [Publisher profile](https://clawhub.ai/user/mariusfit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, JSON, Markdown, CSV, SQLite database records, and incident Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local journal data under the configured ops journal directory and can export reports to user-specified paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
