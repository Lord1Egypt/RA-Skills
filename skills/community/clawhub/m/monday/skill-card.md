## Description: <br>
Monday.com API integration with managed OAuth for managing boards, items, columns, groups, users, and workspaces using GraphQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow operators use this skill to query, create, update, and delete Monday.com boards, items, columns, groups, users, and workspaces through Maton-managed OAuth access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or change Monday.com data through OAuth-backed Maton access when credentials are provided. <br>
Mitigation: Install only if Maton is trusted for this access and approve create, update, or delete operations only after checking the target and effect. <br>
Risk: A leaked MATON_API_KEY could expose connected Monday.com access. <br>
Mitigation: Keep MATON_API_KEY secure and avoid logging, sharing, or committing it. <br>
Risk: When multiple Monday.com connections exist, requests may affect the wrong account. <br>
Mitigation: Verify the intended Maton connection and use the Maton-Connection header for the target account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/monday) <br>
- [Monday.com API Basics](https://developer.monday.com/api-reference/docs/basics) <br>
- [Monday.com GraphQL Overview](https://developer.monday.com/api-reference/docs/introduction-to-graphql) <br>
- [Monday.com Boards Reference](https://developer.monday.com/api-reference/reference/boards) <br>
- [Monday.com Items Reference](https://developer.monday.com/api-reference/reference/items) <br>
- [Monday.com Columns Reference](https://developer.monday.com/api-reference/reference/columns) <br>
- [Monday.com API Changelog](https://developer.monday.com/api-reference/changelog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, GraphQL, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Maton-managed Monday.com OAuth connection.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter metadata.version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
