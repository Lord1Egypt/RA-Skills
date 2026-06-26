## Description: <br>
Manage Linear issues, projects, teams, and documents from the command line using the linear CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cipher-shad0w](https://clawhub.ai/user/cipher-shad0w) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams that use Linear can ask an agent to prepare CLI commands and guidance for managing issues, projects, teams, documents, and Linear GraphQL API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real Linear workspace changes, including creating, updating, and deleting issues, teams, projects, milestones, or documents. <br>
Mitigation: Review generated commands before running them, especially commands that delete resources, operate in bulk, use force flags, or skip confirmation prompts. <br>
Risk: Linear API tokens or authentication output may be sensitive if displayed or copied into commands. <br>
Mitigation: Treat Linear API tokens as secrets, avoid pasting them into shared logs, and prefer the authenticated CLI flow when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cipher-shad0w/openclaw-linear) <br>
- [Issue command reference](references/issue.md) <br>
- [Project command reference](references/project.md) <br>
- [Team command reference](references/team.md) <br>
- [Document command reference](references/document.md) <br>
- [Linear API command reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Linear CLI commands, GraphQL query examples, and review guidance for potentially destructive operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
