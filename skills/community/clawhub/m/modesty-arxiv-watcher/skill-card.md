## Description: <br>
Search and summarize papers from ArXiv when the user asks for the latest research, specific topics on ArXiv, or a daily summary of AI papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill to find recent ArXiv papers by topic, author, category, or paper ID, summarize abstracts, and keep a local research log of discussed papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to ArXiv when the skill queries the ArXiv API. <br>
Mitigation: Avoid confidential or sensitive research topics in queries unless sharing them with ArXiv is acceptable. <br>
Risk: Discussed papers and summaries are persistently appended to memory/RESEARCH_LOG.md. <br>
Mitigation: Review, redact, or clear the research log when working with sensitive projects or before sharing the workspace. <br>


## Reference(s): <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [ArXiv API query endpoint](https://export.arxiv.org/api/query?search_query=all:$QUERY&start=0&max_results=$COUNT&sortBy=submittedDate&sortOrder=descending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown summaries with ArXiv links and a persistent research-log entry] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the ArXiv API and records discussed papers in memory/RESEARCH_LOG.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
