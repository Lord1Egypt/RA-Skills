## Description: <br>
Interact with Linear for issue tracking, including creating, updating, listing, searching, viewing assigned issues, changing status, adding comments, and managing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emrekilinc](https://clawhub.ai/user/emrekilinc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to manage Linear issues from an agent workflow, including listing assigned work, searching issues, creating issues, updating fields, and adding comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create issues, change issue status or assignee, and post comments in a real Linear workspace. <br>
Mitigation: Confirm any create, update, assignment, status-change, or comment action before execution. <br>
Risk: Linear API requests may include untrusted user text in create, update, comment, or search operations. <br>
Mitigation: Avoid passing untrusted text directly into commands and review generated issue titles, descriptions, search strings, and comments. <br>
Risk: The skill requires a Linear API key that can expose or modify workspace data. <br>
Mitigation: Use the narrowest Linear API key available and store it only in the documented credential file or environment variable. <br>


## Reference(s): <br>
- [Linear API Examples](references/api-examples.md) <br>
- [Linear API Key Settings](https://linear.app/settings/api) <br>
- [Linear GraphQL API Endpoint](https://api.linear.app/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional raw JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Linear API key from LINEAR_API_KEY or ~/.clawdbot/credentials/linear.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
