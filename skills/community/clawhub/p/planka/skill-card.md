## Description: <br>
Manage Planka (Kanban) projects, boards, lists, cards, and notifications via a custom Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[voydz](https://clawhub.ai/user/voydz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Planka workspaces from an agent-assisted command line workflow, including listing boards and cards, checking notifications, and creating, moving, updating, or deleting cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install an external planka-cli Homebrew tap. <br>
Mitigation: Install only if the third-party tap and publisher are trusted, and review the CLI before use. <br>
Risk: Passing a real Planka password directly in a shell command can expose credentials through shell history or process inspection. <br>
Mitigation: Prefer an interactive prompt, secure credential storage, or a limited-use Planka account. <br>
Risk: The CLI can create, move, update, or delete Planka cards. <br>
Mitigation: Require confirmation before mutating actions and use an account scoped to the intended boards. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/voydz/planka) <br>
- [Publisher profile](https://clawhub.ai/user/voydz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the planka-cli binary and configured Planka credentials.] <br>

## Skill Version(s): <br>
0.1.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
