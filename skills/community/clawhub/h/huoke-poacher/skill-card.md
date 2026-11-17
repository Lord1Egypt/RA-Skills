## Description:

帮助营销、运营与销售团队检索抖音公开内容、账号、评论和热榜，并整理趋势、竞品、需求与潜在客户线索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

面向营销、运营、内容分析与销售团队，用于检索抖音公开视频、图文、账号、评论和热榜，并整理选题、竞品、舆情、需求或获客线索。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links or IDs may be sent to an external API; the security assessment says this disclosure is unclear.

Mitigation: Review the external-service disclosure before use and submit only query terms and public content identifiers appropriate for that service.

Risk: Broad activation may match generic customer or competitor searches beyond a clear Douyin data request.

Mitigation: Use the skill for explicit Douyin public-data tasks and clarify ambiguous requests before querying.

Risk: The security scan inspected only part of the skill's components.

Mitigation: Review the remaining components before installing or relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/huoke-poacher)
- [GuaiKei API service](https://www.guaikei.com)
- [Customer acquisition guide](references/customer-acquisition.md)
- [Demand mining guide](references/demand-mining.md)
- [Output contract](references/contract.md)
- [Error handling guide](references/errors.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results summarized as concise Markdown prose or tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public Douyin data; summaries should use returned results only.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
