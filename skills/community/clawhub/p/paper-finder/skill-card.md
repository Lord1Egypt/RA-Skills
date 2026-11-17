## Description:

根据主题、篇名、关键词等检索学术文献，返回真实的期刊信息、影响因子和下载链接，找不到就是找不到，绝不编造

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjinhongmy-pixel](https://clawhub.ai/user/wangjinhongmy-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to ask an agent to search academic literature by topic, title, keyword, author, database, publication date, or impact-factor constraints. The skill is intended to return verifiable paper metadata, summaries, citation or journal metrics when available, and official access or download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries may be sent to external academic websites during browser-based searching.

Mitigation: Avoid confidential, unpublished, personally sensitive, or proprietary research terms unless the user intends them to be searched online.

Risk: Search results, impact factors, and citation counts can be incomplete, outdated, or unavailable across academic databases.

Mitigation: Use the returned source links to verify paper metadata and metrics before relying on them for academic, publication, or purchasing decisions.

Risk: The skill may provide access links for paywalled papers, but it cannot grant subscription access.

Mitigation: Use institutional access, publisher pages, or legitimate open-access copies when full text is not publicly available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjinhongmy-pixel/skills/paper-finder)
- [ClawHub publisher profile](https://clawhub.ai/user/wangjinhongmy-pixel)
- [arXiv example record](https://arxiv.org/abs/1706.03762)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [Semantic Scholar](https://www.semanticscholar.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown search results with bibliographic metadata, short summaries, metrics when available, and verified access links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include not-found explanations and suggestions to broaden or refine search criteria.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
