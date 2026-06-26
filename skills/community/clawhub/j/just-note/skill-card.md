## Description: <br>
Manage personal markdown notes -- search, read, create, and append to notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lanthar91](https://clawhub.ai/user/Lanthar91) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to manage persistent personal markdown notes, including listing, searching, reading, creating, and appending notes in an OpenClaw workspace notes folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes persistent markdown notes, which could expose sensitive personal information if users store secrets there. <br>
Mitigation: Avoid storing passwords or highly sensitive secrets in notes and review note content before creating or appending files. <br>
Risk: Ambiguous create or append requests could write content to the wrong note file. <br>
Mitigation: Confirm the target filename and content before create or append operations when the request could be ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lanthar91/just-note) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and note content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates markdown note files in the configured persistent notes folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
