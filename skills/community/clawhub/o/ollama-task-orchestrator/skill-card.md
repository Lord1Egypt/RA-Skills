## Description:

Manage and execute Ollama tasks via SSH on a remote worker, providing queue status, exclusive task locking, and code generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajeshhuria](https://clawhub.ai/user/rajeshhuria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check a remote Ollama worker, run local-model code generation, write generated code to configured project files, run tests, and inspect available worker projects through SSH.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad SSH-based shell, file-write, and process-control capability on a worker machine.

Mitigation: Install it only on a dedicated low-privilege worker account with isolated non-production project directories and tightly controlled SSH access.

Risk: The exec and natural-language execution paths can run shell commands if enabled or called directly.

Mitigation: Disable or remove exec and NL exec unless they are required, and review commands before allowing agents to run them.

Risk: Generated writes can modify files in the configured default project.

Mitigation: Keep DEFAULT_PROJECT scoped to disposable or reviewed workspaces, use dry-run mode before writes, and review generated changes before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rajeshhuria/skills/ollama-task-orchestrator)
- [Publisher profile](https://clawhub.ai/user/rajeshhuria)
- [README.md](README.md)
- [README-claude-code.md](README-claude-code.md)
- [Ollama](https://ollama.ai)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown, with shell command output and generated code when invoked through the runner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute SSH commands, call a configured local Ollama API, run tests, and write generated code inside the configured project directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
