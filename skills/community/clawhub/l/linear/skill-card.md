## Description: <br>
Query and manage Linear issues, projects, and team workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ManuelHettich](https://clawhub.ai/user/ManuelHettich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and team operators use this skill to inspect Linear work, create and update issues, manage status, assignment, comments, priority, and summarize team activity from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Linear issues, including creating issues, comments, status changes, assignments, and priorities. <br>
Mitigation: Use the least-privileged Linear token available and require confirmation before write commands are run. <br>
Risk: Cached team metadata may be sensitive in shared environments. <br>
Mitigation: Set LINEAR_TEAMS_CACHE to a private path when team names or keys should not be stored in the default temporary location. <br>


## Reference(s): <br>
- [Linear](https://linear.app) <br>
- [Linear GraphQL API endpoint](https://api.linear.app/graphql) <br>
- [ClawHub skill page](https://clawhub.ai/ManuelHettich/linear) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash command examples and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINEAR_API_KEY; optional LINEAR_DEFAULT_TEAM and LINEAR_TEAMS_CACHE environment variables affect command behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
