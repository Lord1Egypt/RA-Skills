## Description:

LYGO Ollama Army provides local, allowlisted multi-role Ollama helpers that process queue JSON through in-process workers and write local results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

Developers and agent operators use this skill to launch local Ollama workers, enqueue allowlisted prompt-processing tasks, and collect local JSON results without public outbound automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local task directories can act as an input channel that triggers local Ollama processing.

Mitigation: Run the worker only in a trusted local workspace, restrict who can write task JSON, and review queued prompts before processing sensitive content.

Risk: The security summary reports an out-of-scope file write risk.

Mitigation: Keep task IDs and queue inputs trusted, avoid untrusted values for queue_task.py --id, and monitor writes to ollama_queue/, ollama_results/, and command-center task/result directories.

Risk: The security summary reports an unpinned executable installer command.

Mitigation: Use a pinned ClawHub installer version and verify the release before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-ollama-army)
- [ClawHub security audit](https://clawhub.ai/deepseekoracle/skills/lygo-ollama-army/security-audit)
- [Artifact homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-ollama-army)
- [SkillHub FULL operator surface](https://chatagent.ca/lygoskillhub.html#full-lygo)
- [Security reference](references/SECURITY.md)
- [SkillSpector audit reference](references/SKILLSPECTOR_AUDIT.md)
- [Agent contract](references/AGENT_CONTRACT.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text]

**Output Format:** [Markdown guidance with inline shell commands and local JSON task/result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Ollama only; outputs are written under ollama_results/ and ollama_command_center/results/.]

## Skill Version(s):

0.9.0 (source: frontmatter, claw.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
