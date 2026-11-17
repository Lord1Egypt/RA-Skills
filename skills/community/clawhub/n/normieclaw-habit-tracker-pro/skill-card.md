## Description:

Habit Tracker Pro turns an AI agent into a conversational accountability partner that tracks habits, logs check-ins, manages streaks, analyzes patterns, and supports local cross-tool sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to configure conversational habit tracking, daily check-ins, streak tracking, habit stacking, pattern analysis, local exports, and dashboard views for personal routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit names, completions, notes, skip reasons, timestamps, streaks, and inferred patterns may reveal sensitive routine or wellness information stored in local plaintext files.

Mitigation: Install only when this local storage model is acceptable, restrict access to the machine and data directory, and periodically export or delete old data.

Risk: Cross-tool sync can share habit completion data with other local NormieClaw tools.

Mitigation: Review cross-tool sync settings before enabling them and connect only tools that are trusted to read or write habit status.

Risk: Daily check-ins and habit notes can pass through the user's configured chat channel.

Mitigation: Use chat channels whose privacy and retention settings are appropriate for personal behavioral data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/normieclaw-habit-tracker-pro)
- [README](README.md)
- [Security Considerations](SECURITY.md)
- [Dashboard Specification](dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON schemas, shell commands, configuration files, and local report/export text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local habit data files, CSV and markdown exports, weekly summaries, dashboard configuration, and conversational habit-management guidance.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
