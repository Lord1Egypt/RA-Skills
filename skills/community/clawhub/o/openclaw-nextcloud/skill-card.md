## Description:

Manage Notes, Tasks, Calendar, Files, Contacts, and Deck Kanban boards in your Nextcloud instance via CalDAV, WebDAV, Notes, and Deck APIs. Use for creating notes, managing todos and calendar events, uploading/downloading files, managing contacts, and organizing Kanban boards, stacks, and cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keithvassallomt](https://clawhub.ai/user/keithvassallomt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Nextcloud users can ask an agent to read and manage notes, tasks, calendar events, files, contacts, and Deck boards in their Nextcloud account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The app password grants full account-scope access to the user's Nextcloud data.

Mitigation: Use a dedicated, revocable app password and account for its full scope before use.

Risk: Writes, deletes, uploads, and public shares can immediately change or expose account data.

Mitigation: Confirm exact targets and operations before changes; prefer password-protected, expiring read-only shares.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/keithvassallomt/skills/openclaw-nextcloud)
- [Project homepage](https://github.com/keithvassallomt/openclaw-nextcloud)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [CLI text responses and downloaded files in their original formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes Nextcloud account data; requires the instance URL, username, and an app password.]

## Skill Version(s):

0.9.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
