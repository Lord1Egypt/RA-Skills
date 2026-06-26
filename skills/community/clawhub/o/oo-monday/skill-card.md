## Description: <br>
Operate monday.com through an OOMOL-connected account for reading, creating, updating, moving, archiving, and deleting Monday resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to let an agent work with monday.com boards, items, updates, workspaces, users, teams, forms, dashboards, docs, and related resources through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, archive, move, and delete monday.com data. <br>
Mitigation: Review the exact action, target resource, and payload before approving any write or destructive operation. <br>
Risk: A broad trigger may activate the skill when a user mentions Monday as a weekday rather than monday.com. <br>
Mitigation: Confirm the user intends to operate monday.com before running connector actions when the request is ambiguous. <br>
Risk: The skill requires a connected monday.com account and can act with that account's permissions. <br>
Mitigation: Install it only for users who want an agent to operate their monday.com account through OOMOL. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-monday) <br>
- [Monday Homepage](https://monday.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions may return JSON data and execution metadata from the OOMOL CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
