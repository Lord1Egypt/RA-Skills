## Description: <br>
Integrates ChromaDB with Ollama embeddings for long-term memory and auto-recalls relevant context to enhance conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to connect OpenClaw to a ChromaDB memory collection and Ollama embeddings so agents can manually search and automatically recall relevant long-term context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remembered content can be automatically added to future prompts. <br>
Mitigation: Disable autoRecall for sensitive sessions and review or delete stored memories periodically. <br>
Risk: Memory and embedding requests depend on configured ChromaDB and Ollama endpoints. <br>
Mitigation: Keep ChromaDB and Ollama endpoints local or otherwise trusted, and avoid storing secrets in the collection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Broedkrummen/memory-chromadb) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown-formatted text and prepended context blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual search returns filtered ChromaDB results; auto-recall may prepend relevant remembered context before agent turns when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
