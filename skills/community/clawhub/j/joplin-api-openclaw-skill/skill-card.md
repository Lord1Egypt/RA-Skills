## Description:

Manage Joplin notes via Server API - create, read, edit, search notes, notebooks, todos, and kanban boards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slavaboiko](https://clawhub.ai/user/slavaboiko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an agent manage notes, notebooks, TODOs, and kanban-style markdown content in a self-hosted Joplin Server instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Joplin credentials and can expose them if the local configuration file is printed or mishandled.

Mitigation: Do not print ~/.joplin-server-config; prefer 1Password or short-lived environment variables, and keep any config file permissioned to the local user.

Risk: The skill can create, edit, and delete Joplin notes and notebooks.

Mitigation: Confirm note IDs, notebook names, and titles before overwrite or delete operations.

Risk: Using http:// URLs or JOPLIN_SKIP_TLS_VERIFY can expose credentials or note contents to interception.

Mitigation: Use HTTPS and leave TLS verification enabled unless the user explicitly accepts the risk for a self-signed setup.

Risk: The skill uses an unofficial Joplin Server REST API that may change across server versions.

Mitigation: Test ping and login before note operations, and review API behavior after Joplin Server upgrades.

## Reference(s):

- [ClawHub Joplin Skill](https://clawhub.ai/slavaboiko/skills/joplin-api-openclaw-skill)
- [Joplin](https://joplinapp.org)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Joplin Server](https://github.com/laurent22/joplin/tree/dev/packages/server)
- [joppy](https://github.com/marph91/joppy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate against a configured self-hosted Joplin Server and may read, create, update, search, or delete note data.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
