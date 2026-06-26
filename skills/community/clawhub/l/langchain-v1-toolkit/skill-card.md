## Description: <br>
LangChain v1 knowledge skill that explains Runnable and LCEL composition, uniform invoke/stream/batch semantics, and create_agent returning a LangGraph CompiledStateGraph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this knowledge skill for guidance on LangChain v1 Runnable and LCEL patterns, agent migration, structured output, RAG, streaming, model fallback, and PII handling. Server security evidence notes that the packaged instructions also define ZVT finance and backtesting workflows, so users should treat finance behavior as part of this release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a LangChain toolkit while the security summary says its main instructions define finance and backtesting workflows that can install packages, use local data stores, and write outputs. <br>
Mitigation: Review before installing and use only if finance and backtesting behavior is intended, clearly disclosed, and scoped for the environment. <br>
Risk: Finance workflow behavior may involve package installs, recorder runs, file writes, provider credentials, or broker-related access. <br>
Mitigation: Do not permit package installs, recorder execution, file writes, provider credentials, or broker access without explicit review, user approval, and an isolated workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/langchain-v1-toolkit) <br>
- [Doramagic Crystal Page](https://doramagic.ai/zh/crystal/langchain-v1-toolkit) <br>
- [seed.yaml](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include locale-adapted explanations while preserving code identifiers and constraint IDs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; frontmatter metadata version v0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
