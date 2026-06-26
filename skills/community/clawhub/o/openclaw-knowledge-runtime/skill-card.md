## Description: <br>
Build a standalone layered knowledge runtime with typed links across knowledge entries, entities, memories, and reusable assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design or implement layered agent memory systems that retrieve relevant knowledge, connect records through typed links, and write back only durable findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Knowledge stores can accumulate sensitive or low-quality content if memory files are too broad. <br>
Mitigation: Limit the memory files the skill may read or write, and avoid storing secrets, raw logs, full prompt transcripts, or speculative notes in shared or published stores. <br>
Risk: Noisy write-back can reduce retrieval quality over time. <br>
Mitigation: Write back only stable, high-signal findings after successful runs and keep indexes rebuildable. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Examples](examples.md) <br>
- [Reference](reference.md) <br>
- [ClawHub Release Page](https://clawhub.ai/wanng-ide/openclaw-knowledge-runtime) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with JSON schemas, code snippets, and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compact retrieval and write-back design guidance for agent knowledge stores.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
