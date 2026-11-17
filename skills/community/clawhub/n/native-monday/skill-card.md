## Description:

Read and query Monday.com boards, items, workspaces, and users directly via the Monday.com GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeninja23](https://clawhub.ai/user/codeninja23)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to let an agent inspect Monday.com project and team data, including boards, items, workspaces, users, and account details available to the configured token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Monday.com API token that can access boards, items, workspaces, users, and account information available to that token.

Mitigation: Use a least-privileged token or account where possible, and provide the token only in trusted agent sessions.

Risk: Command output can print board contents, item fields, user emails, workspace details, and account information into the agent session.

Mitigation: Avoid running commands against workspaces containing data that should not be exposed in the session transcript.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeninja23/skills/native-monday)
- [Monday.com GraphQL API endpoint](https://api.monday.com/v2)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON from command-line Monday.com API queries, with Markdown setup and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MONDAY_API_TOKEN and python3; query results are limited by command options and token permissions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
