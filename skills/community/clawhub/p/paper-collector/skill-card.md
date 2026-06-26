## Description: <br>
按用户指定的研究方向检索并筛选学术论文，要求阅读摘要后才可纳入结果，并支持期刊清单限制、数量覆盖和可选 Markdown 输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and analysts use this skill to collect recent papers for a defined research topic, screen candidates by abstract, and return cited paper summaries or a Markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches may send research topics and paper queries to external academic or search websites. <br>
Mitigation: Use the skill only when sharing the research topic with those external sites is acceptable. <br>
Risk: The skill can write a Markdown results file when the user supplies a path. <br>
Mitigation: Provide an output path only when local file creation is intended; otherwise let the agent return results in chat. <br>
Risk: Paper relevance can be overstated if candidates are accepted from titles alone. <br>
Mitigation: Require each included paper to have an accessible abstract and an abstract-based relevance note. <br>


## Reference(s): <br>
- [PubMed](https://pubmed.ncbi.nlm.nih.gov) <br>
- [Google Scholar](https://scholar.google.com) <br>
- [Semantic Scholar](https://www.semanticscholar.org) <br>
- [ScienceDirect](https://www.sciencedirect.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown or conversational text with paper metadata, links, abstract-based relevance notes, and short conclusions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local Markdown file only when the user provides an output path; otherwise returns results in chat.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
