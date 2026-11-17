## Description:

Misskey API integration for posting notes and uploading media to Misskey/Fediverse instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasuganosora](https://clawhub.ai/user/kasuganosora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Misskey credentials, post notes, upload media, delete notes, and inspect the authenticated Misskey account from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Misskey API tokens and uploaded files can be sent to an unintended instance because the scripts include a default host.

Mitigation: Set MISSKEY_HOST explicitly for every run and use a least-privilege Misskey token.

Risk: The upload helper has unsafe shell command construction.

Mitigation: Review the script before use and avoid upload.sh until eval-based command construction is removed.

Risk: The delete helper immediately deletes the supplied note ID without confirmation.

Mitigation: Treat delete.sh as destructive and manually verify the target note ID before running it.

## Reference(s):

- [ClawHub Misskey skill page](https://clawhub.ai/kasuganosora/skills/misskey)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command execution may return Misskey note links, file IDs, account details, or API error text.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
