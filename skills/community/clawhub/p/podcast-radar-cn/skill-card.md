## Description:

Discovers, compares, and curates trending or rising Chinese podcasts and episodes from 中文播客榜 using ranking data first and small-scale Xiaoyuzhou enrichment only when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, podcast creators, curators, and distribution researchers use this skill to find current Chinese podcast episodes or shows, benchmark creators, and build recommendation or curation lists. It is intended to synthesize ranking fields, title signals, and limited enrichment into task-shaped guidance rather than raw data dumps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The enrichment helper can fetch arbitrary URLs, which creates network-scope risk in agents with broad network access.

Mitigation: Run enrichment only for trusted Xiaoyuzhou URLs or in a sandbox that cannot reach localhost, private networks, or metadata services.

Risk: Ranking data is weekly and not full-platform coverage, so recommendations may be incomplete or stale.

Mitigation: Present results as ranking-based signals, include freshness context when available, and avoid claiming comprehensive or real-time coverage.

Risk: Open-rate fields can exceed 1 and may be misunderstood as literal probabilities.

Mitigation: Describe open-rate values only as internal ranking signals or omit them when they are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cellinlab/skills/podcast-radar-cn)
- [Publisher profile](https://clawhub.ai/user/cellinlab)
- [Project homepage](https://github.com/XiaohuoluFM/xhlfm-skills/tree/main/skills/podcast-radar-cn)
- [API Notes](references/api.md)
- [Output Modes](references/output-modes.md)
- [Title Signals](references/title-signals.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown or text summaries with optional inline shell commands and JSON excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranking-first output; Xiaoyuzhou enrichment is limited to small candidate sets and capped at 20 URLs per run.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
