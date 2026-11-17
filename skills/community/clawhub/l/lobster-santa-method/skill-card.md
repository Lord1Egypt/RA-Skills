## Description:

Multi-agent adversarial verification with a convergence loop, where two independent review agents must both pass an output before it ships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to add independent adversarial review to high-stakes outputs such as published content, production code, compliance-sensitive material, and customer-facing documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The original task and generated output may be sent to multiple review agents.

Mitigation: Use trusted review agents and approved environments for any confidential, regulated, or customer-sensitive content.

Risk: Dual review and iterative fix cycles can increase token cost and latency.

Mitigation: Reserve full review for high-stakes outputs, use budget caps or sampling for large batches, and escalate when the iteration cap is reached.

Risk: Reviewer quality can degrade if rubrics are vague or if reviewers share context.

Mitigation: Use objective pass/fail criteria, keep reviewers context-isolated, and re-run fresh reviewers after fixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-santa-method)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with workflow steps, pseudocode, prompts, tables, and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review rubrics, independent reviewer prompts, verdict-gating guidance, fix-loop guidance, and escalation criteria.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
