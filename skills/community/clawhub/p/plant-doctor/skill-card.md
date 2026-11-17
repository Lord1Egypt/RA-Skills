## Description:

Expert botany assistant for plant identification, health diagnosis, care advice, watering schedules, propagation, and safe indoor gardening tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Plant owners and indoor gardeners use this skill to identify plants from photos, diagnose visible health problems, generate care cards, track watering schedules, and receive pet or child toxicity warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and local plant tracking can retain room details, photo context, and care history longer than a user expects.

Mitigation: Ask before writing or bulk-updating plant files, keep writes scoped to plants/, and avoid storing sensitive room or photo details unless the user explicitly wants long-term retention.

Risk: The optional dashboard can expose plant photos, home interior details, schedules, or health logs if deployed without access controls.

Mitigation: Add user ownership columns, enable explicit row-level security policies, require authentication, keep image storage private, and use environment variables for dashboard credentials before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/plant-doctor)
- [Artifact README](artifact/README.md)
- [Security guidance](artifact/SECURITY.md)
- [Dashboard companion specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Plant care templates](artifact/config/care-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON plant records, local file updates, setup commands, and dashboard configuration details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local plant collection and care schedule files under plants/ when the user asks the agent to track plants or watering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
