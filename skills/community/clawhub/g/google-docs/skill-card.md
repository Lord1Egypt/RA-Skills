## Description: <br>
Google Docs API integration with managed OAuth for creating documents, inserting text, applying formatting, and managing content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with Google Docs through Maton's managed OAuth proxy, including viewing documents, creating documents, writing text, formatting content, and managing OAuth connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Docs content and OAuth-authorized requests are routed through Maton's API proxy. <br>
Mitigation: Only connect the intended Google account, protect MATON_API_KEY like a password, and revoke access when it is no longer needed. <br>
Risk: Create, update, and delete operations can modify Google Docs content or OAuth connections. <br>
Mitigation: Approve write or delete operations only after checking the target document or connection and the intended effect. <br>
Risk: Multiple Google Docs connections can route a request to the wrong account if the connection is ambiguous. <br>
Mitigation: Specify the intended connection when more than one Google Docs connection is available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/skills/google-docs) <br>
- [Google Docs API Overview](https://developers.google.com/docs/api/how-tos/overview) <br>
- [Google Docs API Get Document](https://developers.google.com/docs/api/reference/rest/v1/documents/get) <br>
- [Google Docs API Create Document](https://developers.google.com/docs/api/reference/rest/v1/documents/create) <br>
- [Google Docs API Batch Update](https://developers.google.com/docs/api/reference/rest/v1/documents/batchUpdate) <br>
- [Google Docs API Request Types](https://developers.google.com/docs/api/reference/rest/v1/documents/request) <br>
- [Google Docs Document Structure](https://developers.google.com/docs/api/concepts/structure) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>
- [Maton API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Google Docs OAuth connection.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
