## Description: <br>
Medical Literature Search helps users search PubMed, CNKI, Wanfang, and other medical literature databases, summarize abstracts, recommend related papers, and build evidence-based PICO search strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hikaruhuimin](https://clawhub.ai/user/hikaruhuimin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External clinicians, medical researchers, medical students, and drug development teams use this skill to locate and organize medical literature across English and Chinese databases. It supports literature reviews, evidence-based medicine searches, article summaries, and comparison tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical literature summaries may be incomplete, outdated, or unsuitable for direct clinical decision-making. <br>
Mitigation: Verify important claims against primary sources or qualified medical professionals before relying on them. <br>
Risk: Accessing subscription literature databases may expose institutional credentials if used in an untrusted runtime environment. <br>
Mitigation: Use trusted environments for database access and avoid entering subscription credentials unless the runtime is trusted. <br>
Risk: Search and ranking choices can miss relevant medical evidence or overemphasize convenient sources. <br>
Mitigation: Review the generated search strategy, include primary sources where possible, and adjust keywords, MeSH terms, and database coverage for high-stakes use. <br>


## Reference(s): <br>
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) <br>
- [CNKI](https://www.cnki.net/) <br>
- [Wanfang Data](https://www.wanfangdata.com.cn/) <br>
- [VIP Chinese Journal Service Platform](https://www.cqvip.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown literature cards, summaries, and comparison tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are typically limited to 10-20 papers and may include titles, authors, journals, publication years, DOIs, links, summaries, and study types.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
