## Description: <br>
This skill provides semantic search over your memory files using a local vector database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[royhk920](https://clawhub.ai/user/royhk920) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Memory Pro to index local memory files and query them with semantic or hybrid search while managing a local search service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index broad workspace memory and core files that may contain private content. <br>
Mitigation: Set MEMORY_PRO_DATA_DIR, MEMORY_PRO_EXTRA_MD_DIRS, and MEMORY_PRO_CORE_FILES to only the content intended for indexing before running the skill. <br>
Risk: Remote reranking can send search queries and selected memory snippets to a configured endpoint. <br>
Mitigation: Keep remote reranking disabled unless the endpoint is trusted and the user accepts that selected content may leave the local machine. <br>
Risk: Generated index artifacts may expose information from indexed memory files if synced or shared. <br>
Mitigation: Store generated index files in a private local directory and avoid syncing or sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/royhk920/memory-pro) <br>
- [Memory Pro README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local memory paths, index artifacts, and optional reranking configuration.] <br>

## Skill Version(s): <br>
2.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
