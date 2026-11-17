## Description:

按用户指定的研究方向检索并筛选学术论文：在期刊官网、预印本平台与学术来源中搜索，必须阅读摘要后才可纳入结果。适用于用户要求查找、收集、筛选或整理某一主题/研究问题/方向的文献；若未提供研究方向则不得执行。支持可选“仅限期刊清单”模式、可选论文数量覆盖、可选 Markdown 输出路径。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and analysts use this skill to collect recent academic papers for a specified research topic, screen candidates by reading abstracts, and receive a concise literature list. It is intended for topic-driven paper collection, optional journal-list filtering, and optional Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics may be sent to external academic and search sites during paper discovery.

Mitigation: Use non-sensitive research queries and review whether the destination sites are appropriate for the work.

Risk: Optional Markdown output can create a file at a user-provided path.

Mitigation: Provide a clear workspace path for file output and review the generated Markdown before reuse.

Risk: The skill may return fewer papers than requested when abstracts cannot be verified or enough relevant papers are not found.

Mitigation: Rely on the reported count of papers whose abstracts were read and verified, and broaden the topic or sources if needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mxingchtongaelofficial2568/skills/paper-collector)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov)
- [Google Scholar](https://scholar.google.com)
- [Semantic Scholar](https://www.semanticscholar.org)
- [ScienceDirect](https://www.sciencedirect.com)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown or conversational text with paper titles, authors when available, year, venue or platform, links, abstract-based relevance notes, and concise conclusions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default target is 5 papers; Markdown file output requires a user-supplied path or falls back to chat output.]

## Skill Version(s):

0.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
