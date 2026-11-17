## Description: <br>
Linear API引擎(免费版) helps agents manage Linear issues, cycles, projects, and workflow updates through Linear's GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project operators use this skill to generate and run Linear GraphQL queries or mutations for issue tracking, cycle planning, project reporting, and workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to perform broad live Linear API write operations, including issue creation, updates, relabeling, assignment, and batch changes. <br>
Mitigation: Require the agent to show the exact GraphQL request and receive explicit approval before executing any mutation or batch operation. <br>
Risk: A Linear API key could expose workspace data or allow unintended changes if overprivileged or leaked. <br>
Mitigation: Use a dedicated low-privilege Linear API key, keep it out of version control, and revoke or rotate it if exposure is suspected. <br>
Risk: The optional callback_url parameter can send result data to an external destination. <br>
Mitigation: Avoid callback_url unless the destination is trusted and the data that will be sent is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-api-free) <br>
- [Linear](https://linear.app) <br>
- [Linear GraphQL API endpoint](https://api.linear.app/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with curl and GraphQL examples plus JSON response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Linear account, a Linear API key, and network access to the Linear GraphQL API; live mutations should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
