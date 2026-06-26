## Description: <br>
Create and manage modular portable database pods using SQLite metadata and embeddings, including document ingestion and semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[init-v](https://clawhub.ai/user/init-v) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users can use this skill to create local portable knowledge-base pods, ingest documents, store notes, run text or semantic searches, and export pods for sharing or transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist, modify, and export private documents in a local knowledge base with weak guardrails. <br>
Mitigation: Use narrow reviewed folders, avoid sensitive or confidential documents until controls are improved, and review exports before sharing. <br>
Risk: The advertised consent layer may not enforce access for normal queries. <br>
Mitigation: Do not rely on consent commands as the only control; verify pod contents and access paths before querying or sharing data. <br>
Risk: Raw SQL and archive import/export features can expose or alter pod data. <br>
Mitigation: Run raw SQL only for intentional administration and inspect ZIP, .vpod, and Markdown exports before reuse or distribution. <br>


## Reference(s): <br>
- [Agent Consent Layer Technical Spec](REFERENCES/consent-layer-spec.md) <br>
- [Data Pods Usage Reference](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local file outputs from Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and modifies local SQLite pods, metadata files, embeddings, and exported ZIP or .vpod archives.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
