## Description: <br>
Guides developers through integrating HuiMemory, a local semantic memory system, into AI applications for conversation memory, semantic retrieval, and time-filtered recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neko1688](https://clawhub.ai/user/neko1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add HuiMemory-based long-term conversation memory, semantic search, time filtering, and LLM recall tools to AI applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-term conversation history, which can expose sensitive user data if memories are recalled without clear boundaries. <br>
Mitigation: Require explicit user consent before recall, restrict memory by user and session, and define deletion and retention rules. <br>
Risk: Examples can pass recalled conversation history to hosted LLM APIs. <br>
Mitigation: Redact sensitive content and avoid sending recalled history to hosted LLM APIs unless users have clearly accepted that transfer. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neko1688/huimemory-integration) <br>
- [HuiMemory Source Repository](https://gitee.com/HuiMengAI/hui-memory.git) <br>
- [Architecture Reference](references/architecture.md) <br>
- [API Reference](references/api-reference.md) <br>
- [LLM Integration Guide](references/llm-integration.md) <br>
- [BAAI bge-base-zh-v1.5 Model](https://gitcode.com/hf_mirrors/BAAI/bge-base-zh-v1.5.git) <br>
- [BAAI bge-small-zh-v1.5 Model](https://gitcode.com/hf_mirrors/BAAI/bge-small-zh-v1.5.git) <br>
- [BAAI bge-m3 Model](https://gitcode.com/hf_mirrors/BAAI/bge-m3.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, JSON tool schemas, and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes integration patterns, retrieval API examples, prompt templates, and privacy-sensitive memory handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
