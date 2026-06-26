## Description: <br>
Live OmniFocus access via native Omni Automation for tasks, projects, inbox, tags, due dates, flagged items, search, review, and task changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberscribe](https://clawhub.ai/user/cyberscribe) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent query and manage a live OmniFocus 3 or 4 database on macOS through command-line access. It supports task review, search, inbox and project inspection, and authorized task creation or modification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live access to personal OmniFocus data, including write and delete operations. <br>
Mitigation: Install it only when that access is intended, keep write authorization in once or every mode, and require explicit confirmation before delete or bulk edits. <br>
Risk: Invocation may fail or target the wrong entrypoint if the installed command path is not present. <br>
Mitigation: Verify the installed command path before granting write access, or call the reviewed Python script directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberscribe/omnifocus4) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON to stdout; write commands require authorization unless configured otherwise.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
