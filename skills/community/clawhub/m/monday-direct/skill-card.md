## Description: <br>
Interact directly with the monday.com GraphQL API with no third-party gateway, using the official client to read and create boards, items, columns, updates, and users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonah-saltzman](https://clawhub.ai/user/jonah-saltzman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and monday.com workspace operators use this skill to ask an agent to query boards, inspect tasks, and prepare or run GraphQL operations against a live workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent direct monday.com GraphQL access to a live workspace, including operations that can create, update, delete, or change status data. <br>
Mitigation: Use a least-privileged monday.com token and manually confirm create, update, delete, status-change, user, board, or column operations before they run. <br>
Risk: The required monday.com API token could expose workspace data or write authority if it is logged, committed, or shared broadly. <br>
Mitigation: Keep MONDAY_API_TOKEN out of source control and logs, and provide it through the runtime environment or approved secret injection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jonah-saltzman/monday-direct) <br>
- [Using monday.com API Client Libraries](references/api-client-best-practices.md) <br>
- [monday GraphQL API Best Practices](references/graphql-api-best-practices.md) <br>
- [Backend Usage Rules](references/backend-usage-rules.md) <br>
- [monday.com API client package](https://www.npmjs.com/package/@mondaydotcomorg/api) <br>
- [monday.com API release notes](https://developer.monday.com/api-reference/docs/release-notes) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, GraphQL snippets, and JSON API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MONDAY_API_TOKEN; optional MONDAY_API_ENDPOINT and PLATFORM_API can override endpoints.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
