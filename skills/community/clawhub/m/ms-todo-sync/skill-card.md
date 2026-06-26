## Description: <br>
A CLI skill to manage Microsoft To Do tasks via Microsoft Graph API, including listing, creating, completing, deleting, searching, viewing, and exporting tasks and lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoski](https://clawhub.ai/user/xiaoski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this skill to manage Microsoft To Do lists and tasks from a command-line workflow after authenticating with Microsoft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Microsoft To Do data for the account the user authenticates. <br>
Mitigation: Install and run it only when the user accepts Microsoft To Do read/write access, and use logout when cached authentication should be removed. <br>
Risk: Delete commands can remove tasks or task lists. <br>
Mitigation: Avoid the -y option unless deletion intent is clear and confirmed. <br>
Risk: Exports and debug output can expose task content or account activity in shared locations. <br>
Mitigation: Store exports in a private path and do not enable --debug in shared logs or CI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoski/ms-todo-sync) <br>
- [Microsoft Graph API endpoint](https://graph.microsoft.com/v1.0) <br>
- [Microsoft device login](https://microsoft.com/devicelogin) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [CLI text output and optional JSON export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft account authentication and network access to Microsoft Graph.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md metadata, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
