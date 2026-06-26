## Description: <br>
Mistral and Codestral helps agents guide local use of Mistral Large, Mistral-Nemo, Codestral, and Mistral-Small through an Ollama Herd fleet router. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up, query, and monitor local Mistral and Codestral models through a fleet router. It provides shell commands, Python and curl examples, hardware guidance, and guardrails for model downloads and local service use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party ollama-herd package and its publisher. <br>
Mitigation: Install only from a trusted source, review the package before use, and prefer an isolated Python environment. <br>
Risk: Local image, audio transcription, embedding, and chat endpoints could be exposed beyond the intended host if the router is misconfigured. <br>
Mitigation: Keep the localhost service off untrusted networks and restrict access to the local machine or trusted network segment. <br>
Risk: Mistral model downloads can be large and may consume significant storage, memory, and network bandwidth. <br>
Mitigation: Require explicit user confirmation before pulling or deleting models and verify hardware capacity before running large models. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/mistral-codestral) <br>
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local endpoint examples, model and hardware notes, monitoring commands, and guardrails for model download and deletion confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
