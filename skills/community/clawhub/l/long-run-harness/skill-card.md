## Description: <br>
Helps build a runnable Planner-Generator-Evaluator multi-agent harness or long-running orchestrator for app-building workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[is-xins-xiaobai](https://clawhub.ai/user/is-xins-xiaobai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold and configure an autonomous development harness with planner, generator, evaluator, state handoff, evidence collection, workspace boundaries, and iteration controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated harness can write files, run commands, call LLM providers, evaluate local apps, and optionally create git checkpoints. <br>
Mitigation: Use throwaway or clearly scoped workspaces, review generated configuration before full-auto modes, and keep write allowlists and protected paths explicit. <br>
Risk: The skill requires sensitive credentials for selected providers. <br>
Mitigation: Provide only the API keys needed for the selected backend and avoid exposing production secrets or real production URLs during evaluation. <br>
Risk: Autonomous evaluators and generators can produce incorrect changes or over-trust generated evidence. <br>
Mitigation: Review generated plans, configs, diffs, evidence, and evaluator results before deploying or merging harness output. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe harness files, prompts, config, workspace policies, evaluation evidence, and git safety controls.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
