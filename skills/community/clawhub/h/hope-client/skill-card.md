## Description: <br>
Hope Client helps agents make authenticated requests to Hope Server Max APIs for channel, upload, download, account, and engine management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linux2010](https://clawhub.ai/user/linux2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query and automate Hope Server Max operational APIs, including channel status, upload/download instances, account records, engine information, and cleanup actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled default credentials and password-based SSH settings may expose or normalize unsafe access patterns. <br>
Mitigation: Replace and rotate bundled credentials before use, remove password-based sshpass defaults, and load secrets only from controlled environment variables or a secrets manager. <br>
Risk: The skill can perform authenticated POST, PUT, refresh, and bulk cleanup operations against Hope Server data. <br>
Mitigation: Use a least-privilege API key and require manual review before running mutating or bulk commands. <br>
Risk: The skill targets an internal Hope Server deployment and may read sensitive operational data. <br>
Mitigation: Install only in environments where the operator controls the Hope Server target and network path. <br>


## Reference(s): <br>
- [Hope Client on ClawHub](https://clawhub.ai/linux2010/hope-client) <br>
- [Common Queries](references/common-queries.md) <br>
- [Response Format Reference](references/response-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Hope Server environment variables and may issue authenticated SSH-backed API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
