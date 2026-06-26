## Description: <br>
自动检索学术文献（Semantic Scholar/arXiv/CrossRef），进行相关性筛选、主题聚类分析，并生成综述草稿（支持本地模板或大模型润色）。适用于快速了解某个研究方向的前沿动态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical teams use this skill to quickly survey a research topic by retrieving papers from public scholarly APIs, filtering and clustering results, and drafting a structured literature review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: If optional LLM writing is enabled, paper abstracts and generated prompts may be sent to the configured LLM provider. <br>
Mitigation: Review config.json before use and set llm_api_base only to a trusted provider; keep use_llm_for_writing disabled when external processing is not acceptable. <br>
Risk: Outdated dependencies, especially document-output libraries, can introduce avoidable security exposure. <br>
Mitigation: Keep dependencies current, particularly python-docx when DOCX output is enabled. <br>
Risk: Extending the skill to parse untrusted local documents would add a higher-risk input surface. <br>
Mitigation: Add input validation and document-parser hardening before expanding the skill beyond public paper API metadata and abstracts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/paudyyin/literature-review-automator) <br>
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [arXiv API Query Endpoint](http://export.arxiv.org/api/query) <br>
- [CrossRef Works API](https://api.crossref.org/works) <br>
- [Configured LLM API Base](https://api.deepseek.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports by default, with configurable Markdown, DOCX, or TXT file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured review sections, topic clusters, trend summaries, and reference lists based on retrieved paper metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
