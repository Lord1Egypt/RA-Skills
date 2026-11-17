## Description:

OpenPaperGraph helps agents search academic literature, build and analyze citation networks, parse PDFs, import Zotero data, generate research summaries, and export results as structured files or interactive HTML graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahaowugit](https://clawhub.ai/user/jiahaowugit)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and research assistants use this skill to discover papers, build citation graphs from papers or PDFs, analyze literature trends, and export research artifacts for reference managers, reports, or interactive review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The interactive server can expose unauthenticated persistent graph editing beyond localhost.

Mitigation: Run serve mode only on trusted local machines or networks, avoid shared or untrusted networks, and keep backups of graph JSON files before editing.

Risk: Research data, PDFs, metadata, and summaries may be sent to external academic APIs or optional LLM providers.

Mitigation: Avoid processing sensitive unpublished PDFs or private libraries unless external transmission is acceptable, and use extractive summaries or vetted providers for confidential work.

Risk: Dependency installation and API-backed retrieval can introduce supply-chain and service-policy exposure.

Mitigation: Install in a controlled environment with pinned versions where possible, review dependencies before installation, and configure only the API keys needed for the workflow.

## Reference(s):

- [OpenPaperGraph ClawHub release](https://clawhub.ai/jiahaowugit/skills/openpapergraph)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [GROBID](https://github.com/kermitt2/grobid)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [JSON stdout with optional saved BibTeX, CSV, Markdown, JSON, and HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can read local PDFs or graph files, call academic and optional LLM APIs, and persist graph edits to local JSON files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
