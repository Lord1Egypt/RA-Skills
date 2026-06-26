## Description: <br>
Run LangChain AI pipelines locally with Ollama and a local model for coding, DevOps, chat, and document-grounded question answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manojrammurthy](https://clawhub.ai/user/manojrammurthy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run local LangChain/Ollama workflows for code generation, shell-command guidance, concise chat, and document-grounded answers without relying on a cloud model API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DevOps mode can generate shell commands that may change the local system if executed blindly. <br>
Mitigation: Review generated commands before running them, especially commands involving sudo, Docker, Nginx, package managers, or filesystem changes. <br>
Risk: Unpinned LangChain and Ollama-related Python dependencies can change behavior over time. <br>
Mitigation: Install in a virtual environment and pin dependency versions when reproducibility or dependency control matters. <br>
Risk: Generated code, shell guidance, or document-grounded answers may be incomplete or incorrect. <br>
Mitigation: Validate outputs against the target environment and source documents before using them in operational workflows. <br>


## Reference(s): <br>
- [Openclaw Skill Langchain Local ClawHub Page](https://clawhub.ai/manojrammurthy/openclaw-skill-langchain-local) <br>
- [Publisher Profile](https://clawhub.ai/user/manojrammurthy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text streamed from a local LangChain/Ollama chat model; responses may include code blocks, shell commands, or concise guidance depending on mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Ollama at localhost:11434 and uses phi4-mini by default; mode selects coding, devops, chat, or rag prompting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
