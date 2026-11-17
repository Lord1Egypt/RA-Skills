## Description:

Collaboratively design, evaluate, iterate on, and recommend a final launch candidate for a target prompt under a human-gated, agent-executed workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abysscat-yj](https://clawhub.ai/user/abysscat-yj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prompt engineers use this skill to turn prompt design, judge-prompt design, evaluation, iteration, and final launch recommendations into a controlled workflow with human approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Execution Mode can consume API budget or exceed service limits if evaluation runs are not bounded.

Mitigation: Require explicit model, dataset, budget, timeout, retry, and rate-limit boundaries before running evaluations, and use human approval before high-cost iteration loops.

Risk: A high automatic evaluation score may not mean the prompt is ready for launch.

Mitigation: Keep target prompts and judge prompts separate, maintain experiment logs, and require human review of the final launch candidate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abysscat-yj/skills/prompt-design-tuning)
- [Publisher profile](https://clawhub.ai/user/abysscat-yj)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell command, configuration, prompt, evaluation-plan, and report artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution Mode requires user-provided model, dataset, invocation, budget, timeout, retry, and rate-limit boundaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
