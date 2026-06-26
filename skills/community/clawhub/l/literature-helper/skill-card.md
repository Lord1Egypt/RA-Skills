## Description: <br>
文献助手 helps agents find academic papers by topic, author, keyword, or timeframe, and analyze one uploaded PDF with document-grounded summaries and answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyt0302](https://clawhub.ai/user/lyt0302) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic writers use this skill to discover relevant literature, build bilingual search terms, summarize paper metadata, and analyze one uploaded PDF without fabricating unavailable details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marked the bundle suspicious because powerful workflows may run full-access review agents, publish PR artifacts, or perform staff moderation actions. <br>
Mitigation: Install only in a trusted maintainer environment, review full-access defaults before use, prefer lower-privilege modes when available, and run moderation actions only with explicit targets and intended permissions. <br>
Risk: Literature retrieval can mislead users if paper metadata, links, or full-text availability are guessed. <br>
Mitigation: Return uncertainty clearly, label access as open access, repository PDF, abstract only, or unconfirmed, and never claim full-text availability without confirmation. <br>
Risk: PDF question answering can overstate what the uploaded document supports. <br>
Mitigation: Answer primarily from the PDF and state when requested information is not found in the document. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lyt0302/literature-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured literature results include titles, authors, years, sources, summaries, links, and availability labels; PDF analysis is grounded in the uploaded document.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
