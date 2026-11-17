## Description:

Make AI phone calls instantly. No lag, no setup, unlimited scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eypam](https://clawhub.ai/user/eypam)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up agents that place outbound AI phone calls, navigate phone trees, collect call status, and receive transcripts through SDKs, CLI, webhooks, or MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound AI calls can create consent, recording, telemarketing, do-not-call, and jurisdictional compliance obligations.

Mitigation: Confirm the calls are lawful for the target numbers and jurisdictions, obtain consent where required, and avoid telemarketing or do-not-call violations before use.

Risk: Call audio and transcripts may contain sensitive personal data.

Mitigation: Treat call recordings and transcripts as sensitive data, review Pamela's data practices, and avoid sending unnecessary personal or confidential information.

Risk: API keys and billing-enabled accounts can be misused or create unexpected costs.

Mitigation: Use restricted or test API keys while evaluating, keep production keys out of public configs and logs, enable billing alerts, and monitor usage.

Risk: Installing unpinned packages or a global CLI increases supply-chain and local execution exposure.

Mitigation: Verify official package names, prefer pinned versions, and avoid global CLI installation unless it is required and trusted.

## Reference(s):

- [Pamela documentation](https://docs.thisispamela.com)
- [JavaScript SDK reference](https://docs.thisispamela.com/sdk/javascript)
- [Python SDK reference](https://docs.thisispamela.com/sdk/python)
- [Webhook signature verification](https://docs.thisispamela.com/sdk/javascript#verifywebhooksignature)
- [MCP server reference](https://docs.thisispamela.com/sdk/mcp)
- [npm @thisispamela organization](https://www.npmjs.com/org/thisispamela)
- [PyPI thisispamela package](https://pypi.org/project/thisispamela/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell, JavaScript, TypeScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Pamela API subscription and PAMELA_API_KEY.]

## Skill Version(s):

1.1.12 (source: server release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
