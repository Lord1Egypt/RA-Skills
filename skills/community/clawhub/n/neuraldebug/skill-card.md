## Description:

NeuralDebug helps agents debug software across eight languages and inspect or fine-tune transformer models using real debuggers, LLM interpretability commands, and LoRA workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennysun2020](https://clawhub.ai/user/dennysun2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to drive debugger sessions, inspect crashes or runtime state, analyze transformer internals, and run targeted LoRA fine-tuning workflows through agent-readable commands and JSON responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable external code before use.

Mitigation: Install and run it only in an isolated environment after reviewing the cloned repository and dependency changes.

Risk: The skill exposes TCP debug servers and powerful debugger operations.

Mitigation: Bind services to trusted local interfaces, do not expose debug ports to untrusted networks, and require explicit approval before attaching to processes or writing memory.

Risk: LLM analysis and fine-tuning commands can execute model code or create persisted model changes.

Mitigation: Do not run analysis commands on untrusted inputs, and get explicit approval before fine-tuning or persisting model weights across restarts.

## Reference(s):

- [DeepRhapsody Repository](https://github.com/DennySun2020/DeepRhapsody)
- [DeepRhapsody Documentation](https://github.com/DennySun2020/DeepRhapsody/wiki)
- [DeepRhapsody Issues](https://github.com/DennySun2020/DeepRhapsody/issues)
- [Software Debugging Reference](references/software-debugging.md)
- [LLM Debugging Reference](references/llm-debugging.md)
- [LLM Fine-Tuning Reference](references/llm-finetuning.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to start local TCP debug servers, attach to processes, inspect runtime state, execute LLM analysis commands, or run fine-tuning workflows.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
