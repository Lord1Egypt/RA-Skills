## Description: <br>
Google Docs API integration with managed OAuth for creating documents, inserting text, applying formatting, and managing document content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access Google Docs through Maton-managed OAuth for document retrieval, creation, text insertion, formatting, and connection management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or change documents in the connected Google Docs account. <br>
Mitigation: Confirm the selected connection, document ID, target resource, and intended write effect before approving create, update, or delete operations. <br>
Risk: The MATON_API_KEY and Google OAuth connection grant access through Maton. <br>
Mitigation: Keep MATON_API_KEY private, install only if Maton is trusted to proxy requests, and revoke OAuth connections that are no longer needed. <br>
Risk: Multiple Google Docs connections can cause requests to reach the wrong account. <br>
Mitigation: Specify the intended connection when more than one active Google Docs connection exists. <br>


## Reference(s): <br>
- [ClawHub Google Docs Skill](https://clawhub.ai/byungkyu/google-docs) <br>
- [Google Docs API Overview](https://developers.google.com/docs/api/how-tos/overview) <br>
- [Google Docs Batch Update](https://developers.google.com/docs/api/reference/rest/v1/documents/batchUpdate) <br>
- [Google Docs Request Types](https://developers.google.com/docs/api/reference/rest/v1/documents/request) <br>
- [Google Docs Document Structure](https://developers.google.com/docs/api/concepts/structure) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, JavaScript, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require MATON_API_KEY and a selected Google Docs OAuth connection.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
