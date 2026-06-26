## Description: <br>
Performs semantic security analysis and stress testing of AI agent prompts using local Ollama embeddings, STC scoring, and multi-node routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to analyze AI agent prompts or incident-style questions locally, classify them through Mordred's semantic security nodes, and review STC scores and optional Gemma risk output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analyzed prompts are sent to the user's local Ollama service, which may log or store sensitive text depending on local configuration. <br>
Mitigation: Use only controlled local Ollama instances and avoid entering secrets, proprietary incident details, or regulated data unless logging and retention are acceptable. <br>
Risk: The documented --stress and --gemma options do not match the current script behavior. <br>
Mitigation: Test CLI behavior before relying on those modes in a workflow and treat generated risk labels as advisory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/mordred-security-sandbox) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [kit.md](artifact/kit.md) <br>
- [TESTS.md](artifact/tests/TESTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command-line analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Ollama service and the nomic-embed-text model; optional Gemma output is generated locally.] <br>

## Skill Version(s): <br>
4.1.1 (source: server release metadata; artifact documentation identifies v4.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
