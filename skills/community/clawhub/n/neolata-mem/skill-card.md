## Description: <br>
Graph-native memory engine for AI agents with hybrid vector and keyword search, biological decay, Zettelkasten linking, trust-gated conflict resolution, explainability, episodes, compression, and consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jeremiaheth](https://clawhub.ai/user/Jeremiaheth) <br>

### License/Terms of Use: <br>
Elastic-2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent, searchable, local-first memory to agents across sessions, including graph links, decay, conflict handling, and recall workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain sensitive or regulated information if agents store it. <br>
Mitigation: Avoid storing secrets or regulated data, scope agents carefully in shared environments, and start with local or in-memory mode during evaluation. <br>
Risk: Optional Supabase, external embedding or LLM providers, and webhook integrations can send memory content outside the host. <br>
Mitigation: Enable only trusted destinations and use local JSON storage with local or disabled embeddings when data should remain on the host. <br>
Risk: Webhook write-through creates an explicit data exfiltration path. <br>
Mitigation: Configure webhook write-through only for trusted endpoints, or leave it disabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jeremiaheth/neolata-mem) <br>
- [Homepage](https://github.com/Jeremiaheth/neolata-mem) <br>
- [Repository](https://github.com/Jeremiaheth/neolata-mem) <br>
- [npm package](https://www.npmjs.com/package/@jeremiaheth/neolata-mem) <br>
- [neolata-mem User Guide](references/guide.md) <br>
- [Practical Implementation Notes](references/implementation-notes.md) <br>
- [Runtime Helpers](references/runtime-helpers.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents in using a Node.js memory library that stores local JSON data by default and supports optional external storage, embedding, LLM, and webhook integrations.] <br>

## Skill Version(s): <br>
0.8.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
