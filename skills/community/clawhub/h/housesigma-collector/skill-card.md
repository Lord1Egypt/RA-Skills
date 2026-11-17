## Description:

Collects HouseSigma listing data and stores it in a Hauscout SQLite database, supporting automated, profile-based, targeted, and manual collection workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonim1](https://clawhub.ai/user/sonim1)

### License/Terms of Use:


## Use Case:

Developers and operators maintaining a Hauscout property dashboard use this skill to collect HouseSigma listing data, update local SQLite records, manage search profiles, and schedule recurring collection runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated collection writes to the Hauscout SQLite database and could damage or overwrite important data if the database path or collected fields are wrong.

Mitigation: Confirm the target database path, keep backups, and validate collected fields before writes.

Risk: The workflow includes git commit and push steps for database updates, which could publish private, licensed, proprietary, or personal data to the configured remote repository.

Mitigation: Review database contents and remote visibility before enabling git push or scheduled cron updates.

Risk: Automated browsing against HouseSigma can trigger rate limits or blocking.

Mitigation: Use conservative request pacing, troubleshoot with headed mode when needed, and confirm the collection pattern is acceptable for the target site.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sonim1/skills/housesigma-collector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with bash and SQL command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local filesystem paths, database writes, browser automation options, cron scheduling guidance, and git publishing steps that should be verified before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
