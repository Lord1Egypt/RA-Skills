## Description: <br>
hxxra helps agents search, download, analyze, report on, and save research papers using arXiv, Google Scholar, LLM analysis, Markdown reports, and Zotero. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxlhyx](https://clawhub.ai/user/cxlhyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to run paper-discovery workflows, download PDFs, summarize paper content with an LLM, generate Markdown reports, and save selected papers to Zotero collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send paper text or metadata to external LLM and Zotero services when those features are invoked. <br>
Mitigation: Do not use confidential, unpublished, licensed, or personal PDFs unless the configured provider and retention policy are acceptable. <br>
Risk: API credentials may be required for Zotero and LLM analysis. <br>
Mitigation: Use environment variables or a dedicated local config, avoid sharing config files containing real keys, and prefer a dedicated workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxlhyx/hxxra) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>
- [Zotero API key settings](https://www.zotero.org/settings/keys/new) <br>
- [OpenAI-compatible API base URL](https://api.openai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [JSON command responses, Markdown reports, downloaded PDF files, and analysis JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses stdin/stdout JSON commands and may create workspace files for searches, papers, analyses, reports, and logs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, changelog, and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
