## Description: <br>
Interface for managing Joplin notes via WebDAV, including listing notebooks and notes, reading note content, and creating or updating notes and notebooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Martin004](https://clawhub.ai/user/Martin004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect and manage a Joplin database synchronized through WebDAV, including listing notebooks, reading note content, and creating or updating notes or notebooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and overwrite synced Joplin notes using stored WebDAV credentials. <br>
Mitigation: Use a dedicated, least-privilege WebDAV account, verify note and notebook IDs before writes, and keep backups before enabling write operations. <br>
Risk: An agent could run write scripts against sensitive notes with limited safeguards. <br>
Mitigation: Review proposed write operations before execution and avoid automatic writes to sensitive notebooks. <br>


## Reference(s): <br>
- [Joplin Notebook IDs Reference](references/notebooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JOPLIN_PASSWORD, JOPLIN_ACCOUNT, and JOPLIN_WEBDAV_PATH environment variables for WebDAV access.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
