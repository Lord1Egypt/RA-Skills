## Description: <br>
Full Linear project management via the Linear GraphQL API for creating, updating, searching, summarizing, and moving issues, cycles, projects, and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdbotworker](https://clawhub.ai/user/clawdbotworker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, project managers, and support teams use this skill to let an agent work with Linear issues, workflow states, cycles, projects, comments, and backlog summaries using their Linear API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Linear workspace items using the user's Linear API key. <br>
Mitigation: Use the least-privileged Linear API key available and install only when agent access to Linear is intended. <br>
Risk: Write commands such as update-issue, move-issue, post-comment, create-project, and sync-commit can modify project management records. <br>
Mitigation: Review requested write actions before running them, especially workflow moves, comments, project creation, and commit-based status synchronization. <br>
Risk: A retained or over-permissioned API key can continue to authorize Linear actions after the skill is no longer needed. <br>
Mitigation: Revoke the Linear API key when the skill is no longer in use or if access should be withdrawn. <br>


## Reference(s): <br>
- [ClawHub Linear Agent release page](https://clawhub.ai/clawdbotworker/linear-agent) <br>
- [Linear API key settings](https://linear.app/settings/api) <br>
- [Linear GraphQL API endpoint](https://api.linear.app/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, markdown, API calls, configuration] <br>
**Output Format:** [Structured JSON responses, plain-English summaries, and markdown comments sent to Linear] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINEAR_API_KEY and acts with the permissions granted to that Linear API key.] <br>

## Skill Version(s): <br>
1.0.2 (source: CHANGELOG and package.json, released 2026-03-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
