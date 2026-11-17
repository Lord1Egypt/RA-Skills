## Description:

PocketBook Cloud library, reading progress, safe batch uploads/downloads, notes, backups, and two-step book management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rommm13](https://clawhub.ai/user/rommm13)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users use this skill to manage a PocketBook Cloud library by searching and browsing books, checking reading status, transferring books, reviewing notes, creating backups, and deleting one resolved book through a two-step confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict with medium confidence and partial analysis: 12 of 13 components were scanned, while some instruction text and local references could not be fully evaluated.

Mitigation: Review the skill permissions, remaining components, and unresolved references before installation; confirm its tool scope and capabilities fit the intended use.

Risk: The skill handles PocketBook passwords, session data, account tokens, authorization headers, and signed download URLs.

Mitigation: Authenticate on the host through hidden terminal input and keep credentials, session contents, authorization headers, and signed URLs out of chat and logs.

## Reference(s):

- [PocketBook Cloud API notes](references/api.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub release page](https://clawhub.ai/rommm13/skills/pocketbook-cloud)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Concise natural language with JSON helper results, shell commands, and file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ebook archives or backup files through the helper when requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
