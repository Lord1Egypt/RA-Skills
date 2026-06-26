## Description: <br>
Archives and indexes large local or Feishu documents by converting them to structured Markdown, splitting them into searchable chunks, and optionally adding LLM-generated summaries for Obsidian workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuanranc](https://clawhub.ai/user/xuanranc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to process large Word, PDF, text, Markdown, or Feishu documents into Obsidian-ready archives, root indexes, chunk JSONL, and processing reports. It is intended for document archiving, retrieval, and optional insight generation when a document is too large for an agent context window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional LLM enrichment can send document chunks to an external endpoint, and the security summary says the privacy controls do not fully match the code. <br>
Mitigation: Use offline archive-only or archive+index modes unless enrichment is intentionally needed; before enabling it, explicitly set DOC_READER_API_URL, DOC_READER_MODEL, DOC_READER_API_KEY, and DOC_READER_ALLOW_EXTERNAL=true and review which chunks will be sent. <br>
Risk: Feishu ingestion requires local Feishu app credentials and OAuth-style access to cloud document content. <br>
Mitigation: Use a least-privilege Feishu account, enable Feishu mode only for documents the user is authorized to fetch, and keep credentials scoped to the configured account. <br>
Risk: Archived document content and indexes are written to a local output vault that may contain sensitive material. <br>
Mitigation: Choose an output directory appropriate for the document sensitivity and use dry-run behavior for daily-note splitting where available before writing managed blocks. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/xuanranc/junyi-doc-reader) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, JSON/JSONL metadata, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs under the user-selected output directory, including source.md, ROOT_INDEX.md, chunks.jsonl, manifest.json, processing_report.md, and optional split files or enrichment indexes.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
