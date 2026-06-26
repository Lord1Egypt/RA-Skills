## Description: <br>
Complete Miro REST API reference for building integrations, automating workflows, and programmatically managing boards, cards, shapes, users, and team resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to reference Miro REST API authentication, endpoints, rate limits, webhooks, examples, and error handling while building integrations or workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples that use POST, PATCH, DELETE, team-member, or webhook endpoints can modify real Miro resources when run with a valid token. <br>
Mitigation: Use least-privilege scopes, test boards, and explicit human review before executing mutating API examples. <br>
Risk: Personal access tokens or OAuth credentials can expose board, user, or team access if logged or committed. <br>
Mitigation: Store tokens in environment variables or a secrets manager, keep them out of logs and source control, rotate them regularly, and revoke unused tokens. <br>
Risk: Webhook examples can expose receiving endpoints or process untrusted events if signature checks are omitted. <br>
Mitigation: Verify webhook signatures, acknowledge quickly, process asynchronously, and delete unused webhooks. <br>


## Reference(s): <br>
- [Miro REST API - Authentication Guide](references/authentication.md) <br>
- [Miro REST API - Complete Endpoint Reference](references/endpoints.md) <br>
- [Miro REST API - Code Examples](references/examples.md) <br>
- [Miro REST API - Webhooks Guide](references/webhooks.md) <br>
- [Miro REST API - Rate Limiting](references/rate-limiting.md) <br>
- [Miro REST API - Error Handling](references/errors.md) <br>
- [Miro REST API - Best Practices](references/best-practices.md) <br>
- [Miro Developer Documentation](https://developer.miro.com/) <br>
- [Miro API Playground](https://developers.miro.com/playground) <br>
- [Miro Status](https://status.miro.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/bigbubbaagent-bot/miro-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with HTTP, JSON, JavaScript, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; does not install code or execute API calls by itself.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
