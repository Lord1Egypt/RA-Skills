## Description:

Evaluates competing hypotheses to identify the simplest explanation that fits the scenario using forensic, academic, or combined parsimony logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aleph23](https://clawhub.ai/user/aleph23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to compare explanations for investigations, troubleshooting, conceptual debates, and research synthesis. It helps count assumptions, check for fallacies, and explain why one hypothesis is more parsimonious than another.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers may steer ordinary analytical conversations toward parsimony-based hypothesis comparison when a different reasoning frame is needed.

Mitigation: Invoke deliberately for hypothesis comparison and ask the agent to account for the user's stated constraints before preferring the simpler explanation.

Risk: Parsimony can become oversimplification if a simpler hypothesis ignores critical evidence.

Mitigation: Use the skill's fallacy and evidence checks; require the selected hypothesis to explain all provided observations and constraints.

## Reference(s):

- [Occam's Razor Analysis on ClawHub](https://clawhub.ai/aleph23/skills/occams-razer-skill)
- [Core Instructions](references/instructions_core.md)
- [Workflow Logic](references/workflow_logic.yaml)
- [Logical Fallacies Reference Guide](references/fallacies.md)
- [Example Scenarios](references/example_scenarios.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Structured JSON with explanatory rationale in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a preferred hypothesis, assumption analysis, logic rationale, and confidence score.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
