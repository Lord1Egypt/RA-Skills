## Description:

Query Kimi Code Plan quota and usage information, including subscription quota, usage percentage, reset time, and API key status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doraohm1](https://clawhub.ai/user/doraohm1)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to have an agent open their Kimi Code account console, check subscription quota and rate-limit usage, and summarize API key status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens an authenticated Kimi Code console and may expose quota and API-key metadata.

Mitigation: Use only with explicit user intent, limit reporting to quota information by default, and avoid running it in shared workspaces.

Risk: The skill can save a console screenshot as quota.png, which may retain sensitive account details.

Mitigation: Avoid saved screenshots unless specifically requested; if screenshots are needed, redact sensitive fields and delete temporary files after use.

## Reference(s):

- [Kimi Code official site](https://www.kimi.com/code)
- [Kimi Code console](https://www.kimi.com/code/console)
- [ClawHub skill page](https://clawhub.ai/doraohm1/skills/kimi-code-quota)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with table entries and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quota percentages, reset times, membership level, model access, API key metadata, and recent usage records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
