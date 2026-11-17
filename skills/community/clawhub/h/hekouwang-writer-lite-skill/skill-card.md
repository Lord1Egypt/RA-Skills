## Description:

免费版中文写作质控：把话说清楚。文档写作、修订、体检与去 AI 味；出处/模态/修订三铁律；四个纯标准库检查器只报告不改写。何时用：要把素材写清楚、改稿，或说「去 AI 味」。写长文与进阶检查属付费版 hekouwang-writer-skill。不用于无素材的营销文案、诗歌、小说。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT No Attribution

## Use Case:

面向使用中文的外部用户，帮助他们把已有素材写成清晰的文档、修订现有文字、检查文档结构，或降低文章中的程式化表达。检查器只报告问题；用户仍需核实事实与来源。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Revisions could introduce unsupported facts or remove uncertainty from the source material.

Mitigation: Check cited sources and preserve qualifiers such as ‘可能’ or ‘待核实’; flag unsupported claims for review.

Risk: Style and document checks may be mistaken for factual or compliance validation.

Mitigation: Treat checker output as writing guidance, and have a knowledgeable reviewer verify factual claims and applicable requirements.

## Reference(s):

- [产品介绍](https://huiyonghkw.github.io/hekouwang-writer-lite-skill/)
- [write-flow.md](artifact/references/write-flow.md)
- [style-rules.md](artifact/references/style-rules.md)
- [deai-flavor.md](artifact/references/deai-flavor.md)
- [blind-read.md](artifact/references/blind-read.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Chinese Markdown prose and plain-text checker reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writing and review results are returned in the conversation; the four Python checkers report findings without editing documents.]

## Skill Version(s):

2.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
