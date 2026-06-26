## Description: <br>
LiteRAG lets agents index, search, inspect, and benchmark large external documentation corpora using independent SQLite knowledge libraries with keyword and vector hybrid retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozi1924](https://clawhub.ai/user/mozi1924) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use LiteRAG to keep large external documentation corpora out of main agent memory while still retrieving, inspecting, indexing, checking status, and benchmarking retrieval quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vector retrieval can send indexed document chunks and search queries to the configured embedding endpoint. <br>
Mitigation: Inspect .literag/knowledge-libs.json before use and set embedding.baseUrl only to a trusted local or remote endpoint. <br>
Risk: Configured library paths may index more files than intended. <br>
Mitigation: Review each library path and exclude rule before indexing so LiteRAG only processes the intended documentation corpus. <br>


## Reference(s): <br>
- [ClawHub LiteRAG release](https://clawhub.ai/mozi1924/literag) <br>
- [LiteRAG usage](references/usage.md) <br>
- [LiteRAG configuration reference](references/configuration.md) <br>
- [LiteRAG optimization playbook](references/optimization-playbook.md) <br>
- [LiteRAG agent prompt templates](references/agent-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads from CLI tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and inspect commands operate against configured SQLite knowledge libraries under workspace .literag paths.] <br>

## Skill Version(s): <br>
0.2.2 (source: frontmatter, skill manifest, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
