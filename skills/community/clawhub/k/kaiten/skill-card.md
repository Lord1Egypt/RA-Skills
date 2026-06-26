## Description: <br>
Manage Kaiten.ru project boards through the Kaiten REST API, including cards, spaces, boards, columns, tags, comments, checklists, and time tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nixprosoft](https://clawhub.ai/user/nixprosoft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to let an agent inspect and operate Kaiten project-management workspaces, including reading boards and cards, creating or updating tasks, moving work across lanes, and managing comments, tags, members, checklists, and time logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Kaiten token to change or delete live board data. <br>
Mitigation: Use a limited Kaiten token where possible, keep the secrets file private, verify saved default board and state before acting, and require explicit confirmation before deletes, moves, member removals, tag removals, or broad updates. <br>


## Reference(s): <br>
- [Kaiten API Reference](references/api-reference.md) <br>
- [Kaiten Developer Documentation](https://developers.kaiten.ru) <br>
- [Kaiten](https://kaiten.ru) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Kaiten REST API operations through curl or the bundled shell helper when the required Kaiten token and domain are configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
