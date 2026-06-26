## Description: <br>
LanceDB long-term memory plugin with BM25 + vector hybrid search (RRF or linear reranking). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeykrug](https://clawhub.ai/user/joeykrug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to replace the built-in LanceDB memory provider with hybrid BM25 and vector recall while retaining memory_store, memory_recall, and memory_forget workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and saved memories may be embedded, stored locally, and later recalled into context. <br>
Mitigation: Use a scoped embedding API key or trusted local-compatible provider, and avoid storing secrets or regulated data unless the embedding provider and retention policy are acceptable. <br>
Risk: Automatic recall or capture can bring stale, sensitive, or unintended memories into agent context. <br>
Mitigation: Review whether autoRecall and autoCapture should be enabled for the environment, and remove unwanted memories through the available forget workflow or retention controls. <br>
Risk: The plugin replaces the built-in LanceDB memory provider at runtime. <br>
Mitigation: Install it only when that override is intended; remove the plugin load path to revert to the bundled provider. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/joeykrug/memory-lancedb-hybrid) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON5 configuration examples; the installed plugin provides OpenClaw memory tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory storage and recall behavior when installed; recalled memories may be injected into agent context.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
