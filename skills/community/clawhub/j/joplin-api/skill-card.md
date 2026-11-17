## Description:

Manage Joplin notes via REST API. Use for creating, reading, updating, deleting, or searching Joplin notes programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Joplin notes, notebooks, and tags from an agent workflow through the Joplin Data API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that export behavior can write outside the documented workspace boundary.

Mitigation: Do not rely on the export-directory restriction until the export code fails closed for paths outside JOPLIN_EXPORT_DIR; keep exports in a reviewed workspace path.

Risk: The skill supports destructive note, folder, and tag operations, including permanent deletion options.

Mitigation: Confirm target IDs and maintain backups before delete operations; reserve permanent deletion for explicitly approved workflows.

Risk: The skill connects to a Joplin Web Clipper endpoint using an API token.

Mitigation: Use a trusted local endpoint or an HTTPS remote endpoint, avoid remote plaintext HTTP, and protect JOPLIN_TOKEN as a credential.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/killgfat/skills/joplin-api)
- [Joplin REST API](https://joplinapp.org/help/api/references/rest_api/)
- [Joplin Search Syntax](https://joplinapp.org/help/apps/search)
- [Joplin Plugin API](https://joplinapp.org/help/api/)
- [API Reference](references/API.md)
- [Configuration Guide](references/CONFIGURATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with command examples and API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, python-dotenv, and a configured JOPLIN_TOKEN for the target Joplin Web Clipper API.]

## Skill Version(s):

0.1.3 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
