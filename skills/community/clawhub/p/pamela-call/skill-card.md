## Description: <br>
Make AI phone calls instantly. No lag, no setup, unlimited scale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eypam](https://clawhub.ai/user/eypam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to help an agent place Pamela AI phone calls for tasks such as appointment scheduling, order checks, customer-support navigation, information gathering, and follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent place real, billable outbound phone calls. <br>
Mitigation: Confirm each recipient, task, expected cost, and legal basis before initiating calls; enable billing alerts. <br>
Risk: The Pamela API key grants access to call functionality and billing. <br>
Mitigation: Protect PAMELA_API_KEY, avoid placing production keys in logs or public configuration, and use restricted or test keys when evaluating. <br>
Risk: Call audio, transcripts, and webhook payloads leave the local environment. <br>
Mitigation: Review Pamela privacy and data practices, secure webhook endpoints, and validate the X-Pamela-Signature header. <br>
Risk: Outbound calling can create consent, policy, or legal exposure if used for unsolicited or non-consensual calls. <br>
Mitigation: Use the skill only for appropriate calls with a valid legal basis and confirmed recipient context. <br>


## Reference(s): <br>
- [Pamela documentation](https://docs.thisispamela.com) <br>
- [JavaScript SDK documentation](https://docs.thisispamela.com/sdk/javascript) <br>
- [Python SDK documentation](https://docs.thisispamela.com/sdk/python) <br>
- [React components documentation](https://docs.thisispamela.com/sdk/react) <br>
- [Widget documentation](https://docs.thisispamela.com/sdk/widget) <br>
- [MCP server documentation](https://docs.thisispamela.com/sdk/mcp) <br>
- [CLI documentation](https://docs.thisispamela.com/sdk/cli) <br>
- [Webhook signature verification](https://docs.thisispamela.com/sdk/javascript#verifywebhooksignature) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API usage guidance for billable Pamela phone calls that require a PAMELA_API_KEY.] <br>

## Skill Version(s): <br>
1.1.12 (source: server release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
