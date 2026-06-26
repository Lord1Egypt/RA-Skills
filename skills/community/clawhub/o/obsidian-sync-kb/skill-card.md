## Description: <br>
Builds a searchable local knowledge base from an Obsidian vault's "笔记同步助手" inbox, then answers with citations, topic cards, update logs, and daily digests for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangkaifeng](https://clawhub.ai/user/pangkaifeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn an Obsidian sync inbox into a retrieval-ready local knowledge base for OpenClaw. It supports index refreshes, cited question answering, topic promotion, update logs, and daily digest generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read configured Obsidian inbox content and store local indexes, query history, topic cards, logs, and daily digests. <br>
Mitigation: Configure it only for vaults intended for this workflow and review generated artifacts before sharing or syncing them. <br>
Risk: Network enrichment can send note-derived URLs or search terms to external sites during index builds. <br>
Mitigation: Set research.enable_network to false or run build-index with --disable-network for private or work-sensitive vaults. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pangkaifeng/obsidian-sync-kb) <br>
- [Publisher profile](https://clawhub.ai/user/pangkaifeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON responses with citations, plus shell commands and YAML configuration for setup and maintenance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local indexes, topic cards, update logs, daily digests, query history, and build reports under the configured vault artifacts and research directories.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
