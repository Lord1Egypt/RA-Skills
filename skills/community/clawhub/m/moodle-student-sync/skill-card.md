## Description:

Sync and summarize student Moodle data including courses, upcoming deadlines, grades, files, and announcements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yerassyl-sailaubay](https://clawhub.ai/user/yerassyl-sailaubay)

### License/Terms of Use:

MIT-0

## Use Case:

Students and education-support agents use this skill to retrieve Moodle course data and turn it into deadline lists, grade summaries, daily digests, and short-term study plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private student records and a Moodle access token.

Mitigation: Use a least-privilege Moodle token, set MOODLE_URL only to the real HTTPS Moodle site, and avoid shared or synced output directories.

Risk: Generated snapshots, digests, grade summaries, and study plans may contain sensitive academic information.

Mitigation: Restrict permissions on generated files and delete snapshots or digests when they are no longer needed.

Risk: Server security evidence flags the release as suspicious because safeguards are under-disclosed and insufficiently constrained.

Mitigation: Review the skill and its configured environment before installation, and confirm the token scope and output path are appropriate for the user account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yerassyl-sailaubay/skills/moodle-student-sync)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [JSON snapshots and Markdown reports with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+, requests, MOODLE_URL, and MOODLE_TOKEN; MOODLE_USER_ID is optional.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
