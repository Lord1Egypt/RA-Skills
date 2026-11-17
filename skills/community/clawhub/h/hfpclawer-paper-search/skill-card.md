## Description:

Discover, download, and organize academic papers from arXiv, HuggingFace Papers, and OpenReview with multi-source search, deduplication, PDF download, Markdown conversion, and optional wiki sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to monitor academic-paper sources, collect relevant papers, download PDFs, convert them to Markdown, and optionally sync results into a local wiki or agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Zotero read/write paths, MCP server registration, local profile use, and monitor daemon behavior can broaden local data access or automation scope.

Mitigation: Review and enable those integrations intentionally; keep private profiles and Zotero identifiers in local gitignored files.

Risk: Unpinned package launches can reduce repeatability or run a different installed tool version than expected.

Mitigation: Prefer pinned package versions for repeatable installs and launches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diamond2nv/skills/hfpclawer-paper-search)
- [Project homepage](https://github.com/diamond2nv/hfpapers-crawler)
- [PyPI package](https://pypi.org/project/hfpclawer/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, YAML configuration examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update local paper stores, PDF files, Markdown files, wiki content, and optional MCP configuration.]

## Skill Version(s):

0.19.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
