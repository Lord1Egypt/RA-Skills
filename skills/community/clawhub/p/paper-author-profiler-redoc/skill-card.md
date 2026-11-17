## Description:

根据论文链接（arXiv / Google Scholar / Nature 等）自动抓取全部作者列表，并行搜集每位作者的公开信息（所在机构、研究方向、教育背景、Google Scholar / GitHub / LinkedIn / 个人主页），生成双 Sheet Redoc 在线文档：Sheet1 为作者个人信息表（含账号链接），Sheet2 为按学校背景分组汇总。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mc6680000](https://clawhub.ai/user/mc6680000)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to turn a paper link for a large multi-author publication into structured author profiles and grouped institutional summaries in a Redoc document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public author-profile data may be inaccurate, stale, or sensitive when aggregated into a shareable document.

Mitigation: Review generated profiles before sharing and keep uncertain details marked as pending confirmation.

Risk: The workflow may search public web sources, use Semantic Scholar, spawn subagents for large papers, and publish results to Redoc.

Mitigation: Install and run the skill only in environments where these network, delegation, and document-publishing behaviors are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mc6680000/skills/paper-author-profiler-redoc)
- [Semantic Scholar Graph API paper authors endpoint](https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=authors)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance and structured two-sheet Redoc document content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles may include public affiliation, research area, education background, Google Scholar, GitHub, LinkedIn, and personal homepage fields; unavailable details are marked as pending confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
