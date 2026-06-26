## Description: <br>
Direct Linear workspace helper using Linear's GraphQL API from native Node.js for listing, reading, summarizing, creating, commenting on, and updating Linear issues, projects, teams, states, priorities, standup notes, and branch names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwestburg](https://clawhub.ai/user/jwestburg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect Linear workspace data and, with explicit approval, create or update Linear issues, comments, priorities, statuses, and projects from a local Node.js command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive API credentials and sends user requests or workspace data to an external service. <br>
Mitigation: Install and run it only with approved credentials, avoid secrets or confidential data unless the disclosure is intentional, and redact workspace-sensitive output before sharing logs. <br>
Risk: Approved write commands can create or modify Linear issues, comments, priorities, statuses, or projects. <br>
Mitigation: Use read-only commands by default and run write commands only when the user explicitly approves the exact action, target, and intended mutation; the script also requires --execute for mutations. <br>


## Reference(s): <br>
- [ClawHub: Linear Native Node](https://clawhub.ai/jwestburg/linear-native-node) <br>
- [Linear GraphQL API endpoint](https://api.linear.app/graphql) <br>
- [Linear API key settings](https://linear.app/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON from Node.js command output, with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write commands require an explicit --execute flag and user approval; list commands return the first page and support bounded limits.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
