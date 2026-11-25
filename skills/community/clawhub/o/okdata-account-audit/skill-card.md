## Description:

Fetches an account profile and its latest page of posts across 11 social platforms, then presents account and post metrics in a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

People checking a social media account can use the skill to retrieve its profile and one page of recent posts, then review account and post metrics together. It supports 11 platforms and reports the cost before paid calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends account lookup requests to api.okdata.online; some referenced material was not covered by the security analysis.

Mitigation: Review the skill's requests and privacy terms, and proceed only if you trust api.okdata.online and accept the information sent.

Risk: The account and posts lookups are paid calls, so running the skill can incur charges.

Mitigation: State the platform-specific call costs before the first call, and get the user's go-ahead before making more than four calls in one run.

## Reference(s):

- [Account Audit Skill (English)](https://okdata.online/skills/account-audit/?src=skill-okdata-account-audit)
- [Account Audit Skill (中文)](https://okdata.online/zh/skills/account-audit/?src=skill-okdata-account-audit)
- [okdata Agent Setup](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Markdown table with account and post metrics, followed by a concise account performance summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One account profile and one page of recent posts per account; unsupported metrics are left blank. Calls are paid and costs are stated before execution.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
