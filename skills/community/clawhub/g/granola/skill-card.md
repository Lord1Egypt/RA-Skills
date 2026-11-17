## Description:

Access Granola meeting transcripts and notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scald](https://clawhub.ai/user/scald)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to sync Granola meeting transcripts, notes, summaries, and metadata to local files for search and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync uses Granola app tokens to download private meeting content in bulk.

Mitigation: Run it only after review, keep the output in a protected local directory, and avoid shared or synced folders unless sharing is intended.

Risk: The optional cron configuration can continue syncing meeting data in the background.

Mitigation: Skip or remove the cron job if ongoing background sync is not desired.

Risk: Meeting transcript and metadata files may contain sensitive attendee, calendar, and meeting information.

Mitigation: Restrict local file permissions and control access to the selected output directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scald/skills/granola)
- [ClawHub Publisher Profile](https://clawhub.ai/user/scald)
- [Granola](https://granola.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and configuration snippets; sync output writes JSON and Markdown meeting files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a signed-in Granola desktop app on macOS; optional recurring sync writes meeting data to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
