## Description:

A powerful model routing skill that analyzes query intent and cost-efficiency to select the optimal LLM tier before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rayray1218](https://clawhub.ai/user/rayray1218)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to classify prompts by semantic intent and route work to Elite, Balanced, or Basic LLM tiers for cost-aware execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full user prompts may be saved locally in plaintext for routing history.

Mitigation: Disable or remove full-query logging before production use, or require explicit opt-in with deletion controls.

Risk: Sensitive prompts could be exposed through local history files.

Mitigation: Avoid using the skill with secrets, credentials, proprietary text, or personal data unless local storage controls are acceptable.

Risk: Runtime dependencies are declared with lower bounds only.

Mitigation: Pin and review dependencies before deploying the skill in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rayray1218/skills/model-selector)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance, Configuration]

**Output Format:** [JSON routing decision with model-tier guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes selected tier, suggested model, confidence score, and per-tier similarity scores when semantic routing is available.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
