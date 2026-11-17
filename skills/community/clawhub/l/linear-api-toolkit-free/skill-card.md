## Description: <br>
Linear Api Toolkit Free helps agents use the Maton CLI and Linear GraphQL API to query Linear issues, projects, teams, cycles, labels, and comments, with basic create and update actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, and team members use this skill to inspect Linear work items, browse project and team state, add comments, and perform basic issue creation or updates from an agent-assisted command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Linear write actions can create, update, delete, or comment on workspace records. <br>
Mitigation: Confirm the target workspace, team, issue, and intended result before any write action; inspect the current issue state before updating it. <br>
Risk: Maton and Linear credentials grant access to workspace data and actions. <br>
Mitigation: Use the documented login and OAuth flow, do not hardcode API keys, and revoke the Maton or Linear connection when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/linear-api-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-shaped result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Maton CLI, a Linear account, OAuth connection setup, and user confirmation before write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
