## Description: <br>
Ingest Paper guides an agent through extracting research materials, classifying them, generating Chinese structured summaries, and saving knowledge-base pages to a per-user Gitea repository with optional Feishu synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research teams use this skill to ingest arXiv papers, GitHub repositories, web pages, uploaded documents, spreadsheets, Markdown/text files, and typed notes into a personal research knowledge base. The agent creates Chinese summaries, concept pages, resource pages, duplicate checks, catalog updates, and optional Feishu table records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Gitea site-admin token, which is broader access than normal repository ingestion should need. <br>
Mitigation: Install only for a controlled Gitea instance, store the token securely, and prefer a dedicated least-privilege bot token if the deployment can be changed to support narrower permissions. <br>
Risk: Saved research summaries, uploaded PDFs, catalog entries, and log.md entries may expose sensitive research material or user activity to anyone with repository access. <br>
Mitigation: Review access to each target Gitea repository and the system-config repository before deployment, and periodically audit generated log and catalog files. <br>
Risk: Optional Feishu synchronization can send document metadata to an external table. <br>
Mitigation: Enable Feishu sync only after user opt-in and verify the configured app token, table ID, and table permissions. <br>


## Reference(s): <br>
- [ClawHub skill page: Ingest Paper](https://clawhub.ai/myd2002/ingest-paper) <br>
- [Publisher profile: myd2002](https://clawhub.ai/user/myd2002) <br>
- [arXiv](https://arxiv.org/) <br>
- [arXiv API query endpoint](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese-language Markdown pages, JSON script results, shell commands, configuration notes, and concise user-facing status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes temporary extraction and draft files under /tmp/paperkb and saves summaries, PDFs, concept pages, resource pages, catalog entries, indexes, and logs to the configured Gitea knowledge base.] <br>

## Skill Version(s): <br>
2.1.1 (source: server evidence release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
