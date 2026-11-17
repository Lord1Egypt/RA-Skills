## Description:

Manage MuPiBox media database (data.json) through the MuPiBox backend API: list, add, remove, move, edit fields, and restore entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomquist](https://clawhub.ai/user/tomquist)

### License/Terms of Use:


## Use Case:

Developers and MuPiBox operators use this skill to inspect and update a MuPiBox media database through its backend API while keeping local backups for mutation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or restore a MuPiBox media database through API mutation commands.

Mitigation: Use it only against intended MuPiBox instances, review proposed add/remove/move/edit operations before execution, and verify changes with list commands.

Risk: The default MuPiBox endpoint uses plaintext HTTP.

Mitigation: Use a trusted or isolated network, and prefer an HTTPS base URL if the MuPiBox deployment supports it.

Risk: Local backup files may contain media metadata.

Mitigation: Review and protect files in ~/.mupibox-db-backups when metadata is sensitive, and restore only from trusted backup files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomquist/skills/mupibox-media-db)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-oriented data operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled Python script can list entries, create backups, mutate MuPiBox records through HTTP API calls, and restore from trusted backup JSON files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
