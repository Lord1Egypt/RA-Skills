## Description: <br>
Manage MuPiBox media database (data.json) through the MuPiBox backend API: list, add, remove, move, edit fields, and restore entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomquist](https://clawhub.ai/user/tomquist) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage MuPiBox media entries through the bundled command-line helper while preserving backups before mutations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add, delete, move, edit, or restore MuPiBox media database entries. <br>
Mitigation: Review each requested mutation before running it and verify changes with the list command afterward. <br>
Risk: Using the wrong base URL could target an unintended MuPiBox backend. <br>
Mitigation: Confirm that --base-url points to the intended MuPiBox backend before running read or write operations. <br>
Risk: Restore operations can replace the current database with untrusted backup JSON. <br>
Mitigation: Restore only from trusted backup files and keep backup files private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomquist/mupibox-media-db) <br>
- [Publisher profile](https://clawhub.ai/user/tomquist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report backup file paths and operation results when the bundled helper is run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
