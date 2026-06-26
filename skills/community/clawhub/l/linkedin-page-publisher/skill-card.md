## Description: <br>
Publishes text, image, multi-image, video, and article-link posts to a LinkedIn Company Page through LinkedIn's versioned REST Posts API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webtaken](https://clawhub.ai/user/webtaken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social or content operations teams use this skill to configure LinkedIn OAuth credentials, dry-run posts, publish content to a LinkedIn Company Page, and troubleshoot LinkedIn Posts API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live content to a LinkedIn Company Page using sensitive OAuth credentials. <br>
Mitigation: Use dry-run mode and explicit human approval before live posting; store access and refresh tokens in a secret manager or tightly permissioned local file. <br>
Risk: The OAuth helper requests broader organization-admin permission than the publishing workflow needs. <br>
Mitigation: Review the LinkedIn consent screen before authorizing and avoid approving organization-admin permissions unless they are specifically required. <br>
Risk: Long-lived LinkedIn tokens may be exposed if copied into logs, shell history, or shared files. <br>
Mitigation: Redact tokens from troubleshooting output and revoke or rotate tokens immediately if exposure is suspected. <br>


## Reference(s): <br>
- [Setup guide](references/setup.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [LinkedIn Developer Apps](https://www.linkedin.com/developers/apps) <br>
- [LinkedIn REST API](https://api.linkedin.com/rest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run JSON request bodies and live LinkedIn post URNs when executed with user-provided credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
