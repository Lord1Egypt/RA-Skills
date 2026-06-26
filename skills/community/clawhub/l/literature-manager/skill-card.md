## Description: <br>
Search, download, convert, organize, and audit academic literature collections for paper libraries, references, PDFs, Markdown conversions, categories, audits, and code or dataset links mentioned in papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsonaEi](https://clawhub.ai/user/IsonaEi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, developers, and research teams use this skill to build and maintain academic literature collections, including paper search, PDF download, PDF-to-Markdown conversion, indexing, resource collection, and audit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform automated external paper lookups and downloads, including Sci-Hub access. <br>
Mitigation: Require explicit user permission before external downloads, and avoid Sci-Hub unless the user confirms the legal and policy implications for their jurisdiction and use case. <br>
Risk: Cron-monitored sub-agent work can continue longer than expected. <br>
Mitigation: Use cron monitoring only with explicit user approval and confirm the monitor is removed after the task completes. <br>
Risk: Auditing untrusted or unusually named directories may expose path-handling issues. <br>
Mitigation: Run audit checks only on trusted literature directories until path handling has been reviewed and fixed. <br>


## Reference(s): <br>
- [ClawHub Literature Manager release page](https://clawhub.ai/IsonaEi/literature-manager) <br>
- [Google Scholar search](https://scholar.google.com/scholar?q=QUERY&as_ylo=YEAR) <br>
- [Europe PMC PDF service](https://europepmc.org/backend/ptpmcrender.fcgi) <br>
- [arXiv API](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or validate PDF, Markdown, README.md, index.json, RESOURCES.md, and resources.json files in a literature collection.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
