## Description: <br>
Query and manage Linear issues, projects, and team workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TerryRen2024](https://clawhub.ai/user/TerryRen2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to inspect Linear issues, projects, priorities, assignments, and daily standup context, and to perform issue workflow actions from an agent-assisted shell session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Linear API key may allow the agent to read and update Linear work items according to the key's permissions. <br>
Mitigation: Use the least-privileged key available and require explicit approval before create, comment, status, priority, or assignment commands. <br>
Risk: Team metadata is cached locally, and the default cache path may be unsuitable on shared systems. <br>
Mitigation: Set LINEAR_TEAMS_CACHE to a private path when using shared machines or multi-user environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TerryRen2024/linear-1-0-0) <br>
- [Linear](https://linear.app) <br>
- [Linear GraphQL API](https://api.linear.app/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINEAR_API_KEY; optional LINEAR_DEFAULT_TEAM and LINEAR_TEAMS_CACHE tune command behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
