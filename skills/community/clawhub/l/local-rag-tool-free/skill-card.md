## Description: <br>
本地文件检索（免费版） helps agents build a local document index, search local content, and inject retrieved context for RAG-style workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and individual users use this skill to create a local searchable knowledge base from documents or code and retrieve relevant context for agent-assisted question answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and index broad local document or code directories, which may expose sensitive files if used in an unrestricted workspace. <br>
Mitigation: Run it only from a dedicated folder, avoid directories containing secrets or sensitive business data, and review the chosen indexing scope before execution. <br>
Risk: Some setup or retrieval flows may rely on agent execution capabilities. <br>
Mitigation: Confirm indexing and exec-based setup steps before they run, and review generated commands before allowing the agent to execute them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/local-rag-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks and structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local indexing commands, configuration examples, retrieval guidance, and structured response examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
