## Description: <br>
Manage Joplin notes via REST API for creating, reading, updating, deleting, and searching notes programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to manage Joplin notes, notebooks, and tags through the Joplin Data API. It supports note retrieval, search, creation, updates, deletion, import, export, and organization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, modify, move, and permanently delete Joplin notes, notebooks, and tags. <br>
Mitigation: Review destructive commands before execution, avoid permanent deletes unless backups exist, and test changes on non-critical notes first. <br>
Risk: The Joplin API token gives broad access to the user's Joplin data. <br>
Mitigation: Keep JOPLIN_TOKEN private, scope the runtime environment tightly, and rotate the token if it may have been exposed. <br>
Risk: The export safety boundary is misleading because out-of-scope export paths are warned about rather than rejected. <br>
Mitigation: Set JOPLIN_EXPORT_DIR to an intended workspace path and manually confirm export destinations until the script enforces the boundary. <br>


## Reference(s): <br>
- [Joplin REST API documentation](https://joplinapp.org/help/api/references/rest_api/) <br>
- [Joplin search documentation](https://joplinapp.org/help/apps/search) <br>
- [Joplin API reference](references/API.md) <br>
- [Joplin configuration guide](references/CONFIGURATION.md) <br>
- [ClawHub skill page](https://clawhub.ai/killgfat/joplin-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Joplin API command guidance and may create, update, delete, import, or export Joplin note data when invoked through its scripts.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
