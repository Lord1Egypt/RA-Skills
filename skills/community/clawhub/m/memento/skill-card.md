## Description: <br>
Memento provides local persistent memory for OpenClaw agents by capturing conversations, extracting structured facts via LLM, and auto-recalling relevant knowledge before each turn while storing data in local SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[braibaud](https://clawhub.ai/user/braibaud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agent users use Memento to give agents persistent local memory, extract durable facts from conversations, and recall relevant knowledge before future turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memento stores conversation history and extracted facts in a local long-term data store. <br>
Mitigation: Protect or periodically delete the ~/.engram data store, and install only when local retention of conversation data is acceptable. <br>
Risk: Conversation text may leave the machine when autoExtract or autoQueryPlanning uses a cloud LLM provider. <br>
Mitigation: Keep autoExtract and autoQueryPlanning off for sensitive work, or configure a local Ollama model when data must remain on the machine. <br>
Risk: Cross-agent recall can reuse shared facts across agent boundaries. <br>
Mitigation: Disable crossAgentRecall when agent memories should remain isolated. <br>
Risk: Migration and deep-consolidation CLIs can read configured local memory paths and alter the long-term store. <br>
Mitigation: Review configured paths and run migration dry-runs before executing write operations. <br>


## Reference(s): <br>
- [Memento on ClawHub](https://clawhub.ai/braibaud/memento) <br>
- [Memento repository declared in skill metadata](https://github.com/braibaud/Memento) <br>
- [Project documentation](docs/PROJECT.md) <br>
- [BGE-M3 GGUF model used for optional semantic search](https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-Q8_0.gguf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown and injected text context with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists recalled facts locally in SQLite and can inject selected memory context before agent prompts.] <br>

## Skill Version(s): <br>
0.6.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
