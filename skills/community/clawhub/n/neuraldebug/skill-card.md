## Description: <br>
NeuralDebug helps agents debug software in eight languages and inspect LLM or transformer behavior using debugger-backed sessions, interpretability techniques, and LoRA fine-tuning workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dennysun2020](https://clawhub.ai/user/dennysun2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose crashes, inspect runtime state, analyze model reasoning, detect hallucination causes, and run targeted LoRA fine-tuning workflows from an agent-assisted debugging interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugger and attach workflows can inspect or modify sensitive running processes. <br>
Mitigation: Use the skill only on programs you are authorized to inspect, avoid attach and write_memory on production processes, and review proposed debugger actions before execution. <br>
Risk: The TCP debug server can expose powerful debugging controls if reachable by untrusted users. <br>
Mitigation: Run the server locally and do not expose its port beyond the trusted host or session. <br>
Risk: Custom LLM analysis and fine-tuning workflows may execute trusted code or write persistent model files. <br>
Mitigation: Run exec_analysis only from trusted code, review or pin the DeepRhapsody repository commit before installation, and track fine-tuned model outputs that may auto-load later. <br>


## Reference(s): <br>
- [Repository](https://github.com/DennySun2020/DeepRhapsody) <br>
- [Documentation](https://github.com/DennySun2020/DeepRhapsody/wiki) <br>
- [Issues](https://github.com/DennySun2020/DeepRhapsody/issues) <br>
- [ClawHub Skill Page](https://clawhub.ai/dennysun2020/neuraldebug) <br>
- [LLM Debugging Reference](references/llm-debugging.md) <br>
- [LLM Fine-Tuning Reference](references/llm-finetuning.md) <br>
- [Software Debugging Reference](references/software-debugging.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and JSON debugger responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and git; some workflows require local debugger tools, model dependencies, or trusted analysis code.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
