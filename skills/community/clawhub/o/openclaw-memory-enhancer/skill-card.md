## Description: <br>
Edge-optimized RAG memory system for OpenClaw with semantic search that automatically loads memory files, provides intelligent recall, and enhances conversations with relevant context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryfcb](https://clawhub.ai/user/henryfcb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add local, cross-session memory, semantic search, and contextual recall to OpenClaw workflows, especially on edge devices such as Jetson and Raspberry Pi. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memories can persist sensitive, confidential, regulated, or personal information and may later be exported, recalled, or included in prompts sent to a configured LLM. <br>
Mitigation: Do not store secrets or regulated data unless persistence and prompt reuse are acceptable; review and redact the memory directory before export or LLM use. <br>
Risk: The ClawHub release evidence includes documentation that references external Python scripts rather than including the runnable implementation in the artifact. <br>
Mitigation: Review the linked project code and scan downloaded scripts before running them in an OpenClaw workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/henryfcb/openclaw-memory-enhancer) <br>
- [Project Homepage](https://github.com/henryfcb/openclaw-memory-enhancer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with command examples and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe local memory files, exported Markdown, and recall context for prompts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
