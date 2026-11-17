## Description:

hxxra helps agents search scholarly sources, download PDFs, analyze papers with an LLM, generate Markdown reports, and save selected papers to Zotero.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxlhyx](https://clawhub.ai/user/cxlhyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research operations teams use this skill to run a paper workflow: search arXiv or Google Scholar, download PDFs, analyze paper content, generate reports, and save selected items to Zotero.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF text and metadata may be sent to the configured LLM provider during analysis.

Mitigation: Use only papers cleared for external processing, configure approved LLM endpoints, and avoid confidential, unpublished, or licensed PDFs unless permitted.

Risk: Downloads can fetch arbitrary URLs from search-result JSON files.

Mitigation: Use trusted search-result files, review URLs before download, and run the skill in a restricted workspace.

Risk: Zotero integration can write to a user's library or group collection.

Mitigation: Use least-privilege Zotero API keys, target only intended collections, and rotate keys if exposed.

Risk: Generated analysis and reports can be incomplete or misleading.

Mitigation: Review generated summaries against the original papers before relying on them for decisions or citations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxlhyx/skills/hxxra)
- [arXiv API endpoint](https://export.arxiv.org/api/query)
- [Zotero API key setup](https://www.zotero.org/settings/keys/new)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Configuration]

**Output Format:** [JSON command responses, downloaded PDF files, analysis JSON files, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write search results, paper folders, analysis files, reports, logs, and Zotero collection updates.]

## Skill Version(s):

1.2.0 (source: server release evidence and skill documentation, released 2026-03-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
