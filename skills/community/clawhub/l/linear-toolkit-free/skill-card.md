## Description: <br>
Linear 工具箱 helps individual developers query and manage Linear tasks, projects, and team workflows, including task lookup, issue creation, comments, status and priority updates, standup summaries, and branch-name generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate a personal or single-team Linear workflow from an agent, including issue lookup, basic issue updates, standup preparation, and Git branch naming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live changes in a Linear workspace, including creating, updating, commenting on, assigning, or delete-style actions. <br>
Mitigation: Use a limited-scope Linear API key where possible and require explicit confirmation before any write operation. <br>
Risk: Loose trigger and safety boundaries may cause the agent to act on Linear data when the user only intended planning or discussion. <br>
Mitigation: Confirm the target team, issue, and intended operation before executing commands that affect Linear. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell-command examples and structured JSON-like responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINEAR_API_KEY and optionally LINEAR_DEFAULT_TEAM; write actions can change live Linear workspace data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
