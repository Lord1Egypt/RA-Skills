## Description: <br>
Set up, diagnose, repair, and quality-test private local OpenClaw semantic memory search using Ollama embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brasco05](https://clawhub.ai/user/brasco05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure, diagnose, and validate local OpenClaw semantic memory search with Ollama embeddings instead of hosted embedding APIs or native node-llama-cpp builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can install software, start services, download an embedding model, and change OpenClaw memory configuration when side-effect flags are used. <br>
Mitigation: Run diagnostic mode first and approve --install and --apply-config only when those changes are intended. <br>
Risk: Exposing Ollama outside trusted local or private networks can create network security risk. <br>
Mitigation: Keep Ollama on localhost when possible and review any custom base URL before applying configuration. <br>
Risk: Quality-test queries and excerpts may appear in terminal output, logs, or agent transcripts. <br>
Mitigation: Avoid sensitive quality-test queries when logs may be captured. <br>


## Reference(s): <br>
- [Ollama Memory Setup README](README.md) <br>
- [Troubleshooting - Ollama Memory Setup](references/troubleshooting.md) <br>
- [Ollama](https://ollama.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/brasco05/ollama-memory-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic steps, installation commands, OpenClaw configuration commands, and quality-test guidance.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
