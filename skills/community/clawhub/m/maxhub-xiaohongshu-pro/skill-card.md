## Description:

Analyzes public Xiaohongshu (RED) notes, users, comments, trends, products, and creator data through MaxHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External content analysts, brand teams, and creator agencies use this skill to research public Xiaohongshu content, audience trends, product feedback, and creator performance. It supports content planning, competitor research, and creator selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates this release suspicious, citing sensitive information sent to a third party and compliance records that claim review or confirmation without verification.

Mitigation: Verify the data path and authorization before use, protect API keys and tokens, and independently confirm compliance claims.

Risk: The security scan is partial because some references could not be resolved.

Mitigation: Review current behavior and unresolved references before deployment.

Risk: PGY queries use POST endpoints and consume query quota.

Mitigation: Confirm the intended query and parameters with the user before making a PGY request.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-xiaohongshu)
- [ClawHub release page](https://clawhub.ai/xiewxx/skills/maxhub-xiaohongshu-pro)
- [MaxHub API service](https://www.aconfig.cn)
- [Xiaohongshu Open Platform](https://open.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Concise text or Markdown summaries based on API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results and analysis; minimize personal data and keep credentials out of outputs.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
