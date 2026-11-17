## Description:

Runs complex prompts through a multi-model deliberation pipeline that drafts, cross-critiques, revises, and synthesizes a final answer with uncertainties and evidence notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prairiedoggg](https://clawhub.ai/user/prairiedoggg)

### License/Terms of Use:


## Use Case:

Developers and advanced users use this skill when a request explicitly opts into complex reasoning to coordinate multiple ACP agents through drafting, critique, revision, and synthesis for ambiguous, high-stakes, or long-form tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and intermediate model outputs may be shared across multiple selected agent sessions.

Mitigation: Avoid highly sensitive prompts unless that sharing is acceptable; prefer explicit complex=true activation, explicit model IDs, and a budget limit.

Risk: Untrusted questions or constraints may contain prompt-injection control phrases.

Mitigation: Use the provided input validation and data-block wrapping behavior before generating prompts or orchestration plans.

Risk: Model failures or strong disagreement can reduce answer quality.

Mitigation: Continue with a single failed model while noting reduced diversity; if multiple models fail, ask whether to retry or switch to single-model mode.

## Reference(s):

- [Multi Model Critique ClawHub page](https://clawhub.ai/prairiedoggg/skills/multi-model-critique)
- [Orchestration Template](references/orchestration-template.md)
- [Output Schema](references/output-schema.md)
- [Prompt Templates](references/prompt-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown final answers or JSON run-plan and result payloads, with optional generated prompt files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-model scores, uncertainties, optional next steps, and runtime controls such as timeout, retries, max rounds, and budget.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
