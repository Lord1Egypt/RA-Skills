## Description: <br>
Kannaka Memory gives agents persistent local memory, recall, dream consolidation, audio perception, and optional swarm coordination through a Rust CLI and OpenClaw tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NickFlach](https://clawhub.ai/user/NickFlach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent memory, memory search, status reporting, dream-style consolidation, audio ingestion, and optional swarm synchronization to OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed extension can execute unsafe shell commands from tool inputs. <br>
Mitigation: Review the installer and generated extension before use, test in an isolated environment, pin the upstream source being built, and require argument-array process execution with strict input validation before normal use. <br>
Risk: Swarm commands and non-local Ollama endpoints can send activity or text outside the machine. <br>
Mitigation: Keep swarm features and remote Ollama endpoints disabled unless that data sharing is intended, and configure endpoints explicitly for the deployment environment. <br>
Risk: Memory deletion and networked actions may change persistent agent state or external state. <br>
Mitigation: Use confirmations or operator review for deletion and networked actions, and keep backups of important memory files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NickFlach/kannaka-memory) <br>
- [Kannaka Memory install source](https://github.com/NickFlach/kannaka-memory) <br>
- [Rust toolchain](https://rustup.rs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown setup instructions and tool text or JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists memory to a local HRM file by default; swarm and remote Ollama settings can send activity or text to configured services.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
