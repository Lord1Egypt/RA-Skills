## Description: <br>
Manage Joplin notes via Server API - create, read, edit, search notes, notebooks, todos, and kanban boards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slavaboiko](https://clawhub.ai/user/slavaboiko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to let an agent manage a self-hosted Joplin Server, including listing, searching, reading, creating, modifying, and deleting notes and notebooks after local credential configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad read, create, edit, search, and delete access to Joplin notes. <br>
Mitigation: Install only when that access is acceptable, prefer a dedicated low-privilege Joplin account where possible, and require explicit confirmation before delete-note actions. <br>
Risk: Joplin credentials are stored locally in ~/.joplin-server-config. <br>
Mitigation: Keep the config file locked down with restrictive permissions and use 1Password retrieval when appropriate. <br>
Risk: Disabling TLS verification can expose note traffic to interception. <br>
Mitigation: Avoid JOPLIN_SKIP_TLS_VERIFY except for trusted local or self-signed setups. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/slavaboiko/joplin-api-openclaw-skill) <br>
- [Joplin](https://joplinapp.org) <br>
- [Joplin Server](https://github.com/laurent22/joplin/tree/dev/packages/server) <br>
- [joppy](https://github.com/marph91/joppy) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON; write operations can create, modify, or delete Joplin notes and notebooks.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
