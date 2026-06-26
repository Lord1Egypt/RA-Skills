## Description: <br>
Knowledge Vault helps an agent ingest linked or uploaded content, produce concise digests, store searchable vault entries, and recall saved knowledge later. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn articles, videos, PDFs, threads, repositories, podcasts, and other content into structured summaries, searchable vault records, collections, exports, and recall answers. It is intended for personal or team research workflows where the user explicitly chooses what to save or digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched or uploaded content may include confidential or personal information that is retained in vault entries or memory summaries. <br>
Mitigation: Use explicit save or digest commands, avoid confidential documents unless storage and retention are understood, and redact sensitive data before any memory write. <br>
Risk: External content can contain prompt-injection text or command-like instructions. <br>
Mitigation: Treat all ingested content as untrusted data, summarize it only, and ignore embedded directives. <br>
Risk: Dashboard, delete, and update workflows can affect retained knowledge if implemented without access controls or recovery paths. <br>
Mitigation: Review those workflows for authentication, confirmations, and backup or recovery controls before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-knowledge-vault) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [README](README.md) <br>
- [Security audit](SECURITY.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Vault configuration](config/vault-config.json) <br>
- [Dashboard specification](dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown chat responses with structured digest sections, JSON vault records, configuration files, and optional shell command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store full extracted text in workspace-relative vault files and may write redacted memory summaries when memory integration is enabled.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
