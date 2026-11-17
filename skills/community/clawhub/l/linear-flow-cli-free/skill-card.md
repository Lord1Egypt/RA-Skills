## Description: <br>
Enables an agent to use the Linear command-line interface to query, create, and update Linear issues, teams, projects, labels, and workflow states with machine-readable JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation agents, Scrum Masters, and DevOps engineers use this skill to operate Linear from a terminal workflow for task lookup, issue creation, status updates, comments, labels, and project or team reads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update live Linear issues, labels, comments, and raw API calls. <br>
Mitigation: Require explicit user confirmation before any write operation and prefer dry-run or preview behavior when available. <br>
Risk: Linear API keys or local authentication files could be exposed through shared logs, chats, or version control. <br>
Mitigation: Avoid printing tokens, keep API keys out of shared transcripts, and add .linear.toml to .gitignore. <br>
Risk: Broad activation language could lead an agent to take project-management actions beyond the user's intended scope. <br>
Mitigation: Constrain use to explicit Linear management requests and confirm target team, project, issue, and intended change before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-flow-cli-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Linear CLI, Linear account access, and agent tool-use capability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
