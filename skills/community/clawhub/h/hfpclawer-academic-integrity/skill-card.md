## Description:

Feed a paper draft to automatically extract citations, verify each one against local, Semantic Scholar, and OpenAlex sources, detect fabricated references, and generate a structured integrity report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, reviewers, and literature-survey authors use this skill to audit paper drafts, URLs, PDFs, and reference sections for citation integrity before submission or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local drafts, PDFs, Zotero configuration, and optional local profile files that may contain confidential research or personal metadata.

Mitigation: Use local or sandboxed documents for sensitive drafts, keep private author lists, ORCIDs, and Zotero IDs in ignored local configuration, and enable only the optional extras and integrations needed for the audit.

Risk: Citation checks depend on local metadata and external services that may be incomplete, delayed, unavailable, or rate limited.

Mitigation: Treat suspected, not-found, fabricated, and error findings as review prompts; manually verify recent papers and configure API keys or local metadata where higher-volume checks are needed.

Risk: Unpinned CLI or MCP launches can run an unexpected package version.

Mitigation: Pin uvx, uv tool, and MCP server package versions when launching optional tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diamond2nv/skills/hfpclawer-academic-integrity)
- [hfpapers-crawler repository](https://github.com/diamond2nv/hfpapers-crawler)
- [hfpclawer PyPI package](https://pypi.org/project/hfpclawer/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces citation-integrity findings such as verified, suspected, not found, fabricated, and error statuses, with recommendations for manual follow-up.]

## Skill Version(s):

0.19.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
