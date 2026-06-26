## Description: <br>
Manage and execute Ollama tasks via SSH on a remote worker, including queue status checks, exclusive task locking, code generation, file writes, tests, and shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rajeshhuria](https://clawhub.ai/user/rajeshhuria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route agent requests to a configured Ollama worker over SSH for local code generation, project file updates, test execution, and worker queue management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad SSH-based authority over files, processes, and shell commands on the configured worker. <br>
Mitigation: Install it only on a dedicated, low-privilege worker account and avoid shared or production machines. <br>
Risk: The explicit exec path can run arbitrary shell commands on the worker. <br>
Mitigation: Remove or block `ollama run exec` where it is not required, and keep natural-language exec routing disabled unless explicitly needed. <br>
Risk: Generated output can be written directly into project files. <br>
Mitigation: Use dry-run mode where practical and review generated writes before relying on them. <br>
Risk: Project context is read from AGENT.md and sent into local generation prompts. <br>
Mitigation: Do not put secrets or sensitive operational data in AGENT.md. <br>
Risk: Updates can change worker behavior and command authority. <br>
Mitigation: Pin and review the source before updating the installed runner. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/rajeshhuria/ollama-task-orchestrator) <br>
- [Artifact README](artifact/README.md) <br>
- [Claude Code and Codex usage guide](artifact/README-claude-code.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style command output; generated code can also be written to files on the configured worker.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected command and configured Ollama worker; status commands report health and locks, generation commands return model text or code, write commands modify project files, and test or exec commands return shell output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
