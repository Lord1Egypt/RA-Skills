## Description:

Junyi Doc Reader converts large local documents and Feishu cloud documents into structured Markdown archives, chunk indexes, optional LLM summaries, and Obsidian-ready files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanranc](https://clawhub.ai/user/xuanranc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and agent users use this skill to archive, index, split, and retrieve large local or Feishu documents as Markdown assets for Obsidian workflows. It is especially useful when source documents exceed the agent context window and need chunked processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private document content may be exposed through optional insights mode or direct use of the enrichment script.

Mitigation: Keep insights mode disabled unless external processing is intended; require explicit user consent and review chunks.jsonl before any LLM enrichment.

Risk: Feishu mode reads local Feishu app credentials and calls Feishu APIs.

Mitigation: Use only a configured account selected by the user, restrict network access to official Feishu API endpoints, and do not log or persist credentials.

Risk: Archive output can mix or overwrite state when reusing an output directory.

Mitigation: Use a fresh output directory for each document and review manifest.json, source_meta.json, and processing_report.md after each run.

Risk: --dry-run may not provide a complete no-write preview for every pipeline path.

Mitigation: Treat dry-run as limited to date-split preview behavior and avoid using it as the sole control for preventing writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanranc/skills/junyi-doc-reader)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown files, JSON/JSONL manifests and indexes, and shell commands for running the document pipeline]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include source.md, converted.md, ROOT_INDEX.md, chunks.jsonl, manifest.json, processing_report.md, optional enriched_chunks.jsonl, optional indexes, and optional daily-note Markdown files.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
