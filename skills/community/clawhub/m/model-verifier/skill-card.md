## Description:

Verify model identity by testing 4 dimensions: knowledge cutoff, safety style, multimodal capability, and thinking language patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[civen-cn](https://clawhub.ai/user/civen-cn)

### License/Terms of Use:


## Use Case:

Developers, evaluators, and operators use this skill as a lightweight checklist for observing whether a model's behavior matches its claimed identity across cutoff, safety style, multimodal, and reasoning-pattern checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-identity checks may be unreliable and should not be treated as proof of which model is running.

Mitigation: Use results as rough observations and corroborate them with provider-side model metadata or platform controls before making trust decisions.

Risk: Recorded Q&A may include conversation context provided during testing.

Mitigation: Avoid including sensitive context in test prompts and review captured transcripts before sharing them.

## Reference(s):

- [ClawHub Model Verifier skill page](https://clawhub.ai/civen-cn/skills/model-verifier)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with verdict and suspicious points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records actual Q&A text as evidence when running checks.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
