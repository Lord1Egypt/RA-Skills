## Description: <br>
Precision journal monitor using ISSN lookup. No tool-switching allowed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenghan66](https://clawhub.ai/user/chenghan66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and literature reviewers use this skill to monitor named journals for recent PubMed articles, using ISSN lookup where available and returning bilingual title summaries with PMID, year, and author metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries PubMed, which may expose journal-monitoring topics to an external service. <br>
Mitigation: Preview queries before execution and use the skill only when external PubMed access is acceptable for the research topic. <br>
Risk: The skill can save large reports to the Desktop when many articles are found. <br>
Mitigation: Ask the agent to preview results first and save only to a user-selected path and filename. <br>
Risk: The bundled PubMed helper uses a placeholder Entrez email value. <br>
Mitigation: Configure an appropriate Entrez email before relying on repeated PubMed requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenghan66/journal-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/chenghan66) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-style bilingual report text with article metadata; supporting script output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create report files when many articles are found.] <br>

## Skill Version(s): <br>
1.0.11 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
