## Description:

Synthesizes member-parent markdown reports into a continuous narrative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanleefumu](https://clawhub.ai/user/deanleefumu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team leads use this skill to turn member-organized markdown status reports into a single daily markdown summary. It reads reports grouped by team member, synthesizes multi-day progress into cohesive narratives, and writes a date-stamped daily output file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recursively from the configured report directory and may summarize markdown files that were not intended for the daily report.

Mitigation: Confirm the source directory contains only markdown reports intended for summarization before running the skill.

Risk: The skill writes a date-stamped summary file and could replace an existing daily summary for the same date.

Mitigation: Ask the agent to check for an existing output file before writing or replacing a daily summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deanleefumu/skills/group-summarizer)
- [ClawHub publisher profile](https://clawhub.ai/user/deanleefumu)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown file with member-name section headers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a UTC+8 date-stamped daily summary to the configured latest_summaries path.]

## Skill Version(s):

1.0.0 (source: server release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
