## Description:

Generates and manages Chinese daily literature reports for life sciences and AI by collecting papers, categorizing them, summarizing abstracts, and formatting Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research operations teams use this skill to automate daily monitoring of PubMed, bioRxiv, and arXiv literature in life sciences and AI, then produce categorized Chinese Markdown reports with summaries and trend notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically share or write generated reports to local shared destinations, Zotero group libraries, and Matrix delivery channels.

Mitigation: Review before installation and disable or remove Matrix sending and any shared-destination writes that are not required for the deployment.

Risk: Zotero integration can write to a configured group library and may use inherited environment variables.

Mitigation: Require an explicit Zotero group ID, use a narrowly scoped Zotero API key, and avoid passing the full environment to external helper scripts.

## Reference(s):

- [Category Standards](references/categories.md)
- [Workflow Guide](references/workflows.md)
- [bioRxiv API endpoint](https://api.biorxiv.org/details/biorxiv/{date_from}/{date_to}/0/json)
- [arXiv Export API endpoint](http://export.arxiv.org/api/query?search_query={query}&max_results={max_results})
- [Zotero API key setup](https://www.zotero.org/settings/keys/new)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates dated literature report files and a latest report index; may also copy reports to ClawLib and write entries to Zotero when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
