## Description: <br>
Provides local search over the Mao Selected Works volumes, with structured, keyword, and optionally configured hybrid retrieval for locating articles and passages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryczq](https://clawhub.ai/user/henryczq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to build a local searchable corpus for 《毛泽东选集》 and retrieve source-grounded articles or passages by volume, chapter, title, or keyword. Hybrid retrieval is available only when the user explicitly configures external embedding and rerank services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional RAG mode can send queries or document chunks to configured external embedding and rerank providers. <br>
Mitigation: Keep the default local keyword mode unless external processing is acceptable, and review provider settings plus API key handling before enabling RAG. <br>
Risk: Indexing and search utility scripts operate on local corpus paths and SQLite indexes. <br>
Mitigation: Run the scripts only against the bundled corpus or intended local paths, and avoid pointing them at unrelated databases or directories. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/henryczq/mao-selected-works) <br>
- [Corpus Format](artifact/references/corpus-format.md) <br>
- [Retrieval Rules](artifact/references/retrieval-rules.md) <br>
- [Output Schema](artifact/references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results should include source fields such as volume, article title, source path, retrieval mode, and snippet when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
