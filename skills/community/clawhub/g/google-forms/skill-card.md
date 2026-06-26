## Description: <br>
Google Forms API integration with managed OAuth for creating forms, adding questions, and retrieving responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to interact with Google Forms through Maton-managed OAuth, including reading form metadata and responses and preparing create or update requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and managed OAuth access to a Google Forms account. <br>
Mitigation: Install only if Maton is trusted to broker access, keep MATON_API_KEY private, and rotate or revoke credentials if exposure is suspected. <br>
Risk: Requests can target the wrong Google account when multiple Google Forms connections are available. <br>
Mitigation: Verify the selected connection and include the Maton-Connection header when more than one account is connected. <br>
Risk: Create, update, or delete requests can change forms, questions, responses, or metadata. <br>
Mitigation: Approve write operations only after checking the exact form ID, target resource, and intended change. <br>


## Reference(s): <br>
- [Google Forms Skill Page](https://clawhub.ai/byungkyu/google-forms) <br>
- [Google Forms API Overview](https://developers.google.com/workspace/forms/api/reference/rest) <br>
- [Get Form](https://developers.google.com/workspace/forms/api/reference/rest/v1/forms/get) <br>
- [Create Form](https://developers.google.com/workspace/forms/api/reference/rest/v1/forms/create) <br>
- [Batch Update Form](https://developers.google.com/workspace/forms/api/reference/rest/v1/forms/batchUpdate) <br>
- [List Responses](https://developers.google.com/workspace/forms/api/reference/rest/v1/forms.responses/list) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with Python, JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Google Forms OAuth account.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
