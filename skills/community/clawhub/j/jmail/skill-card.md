## Description: <br>
Search and analyze the Jeffrey Epstein email archive through jmail.world's Data API, DuckDB/Parquet queries, Web Search API, and file-download helpers without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabudde](https://clawhub.ai/user/fabudde) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, journalists, investigators, and developers use this skill to search public Epstein-related emails, iMessages, documents, photos, people, communication networks, and timelines through jmail.world datasets and helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local shell scripts that contact jmail.world-related domains and cache public archive datasets in /tmp. <br>
Mitigation: Review the scripts before use, run them in an approved environment, and remove /tmp/jmail-cache when cached archive data is no longer needed. <br>
Risk: Download commands can save public archive PDFs or images to user-selected directories. <br>
Mitigation: Use a dedicated output directory and verify document IDs and paths before running download commands. <br>
Risk: The archive contains sensitive public records that could be misused for bulk extraction or profiling. <br>
Mitigation: Use the skill only for lawful, ethical research needs and avoid bulk extraction or profiling outside that purpose. <br>


## Reference(s): <br>
- [Jmail World](https://jmail.world) <br>
- [Official Jmail Docs](https://jmail.world/docs/introduction) <br>
- [Jmail Docs Index for LLMs](https://jmail.world/docs/llms.txt) <br>
- [API Reference](references/api-docs.md) <br>
- [DuckDB Examples](https://jmail.world/docs/duckdb) <br>
- [Datasets & URLs](https://jmail.world/docs/datasets) <br>
- [ClawHub Skill Page](https://clawhub.ai/fabudde/jmail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash and SQL snippets; command output may include JSON, DuckDB tables, PDFs, JPGs, or PNGs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public jmail.world data, may cache Parquet files under /tmp/jmail-cache, and can save downloaded documents or photos to user-selected directories.] <br>

## Skill Version(s): <br>
1.6.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
