## Description:

Turns vague or underspecified user requests into structured, actionable prompts using a four-part framework for role, task, context, and constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flonerze](https://clawhub.ai/user/flonerze)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers can use this skill to convert brief Chinese, English, or mixed-language requests into clearer prompts before handing work to an AI assistant or human collaborator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect the original task to be completed immediately, while this skill intentionally returns only a refined prompt.

Mitigation: Present the refined prompt as an intermediate artifact and run it separately with an agent or collaborator when execution is desired.

Risk: For vague requests, the refined prompt may include assumptions that do not match the user's real constraints.

Mitigation: Review and adjust inferred context, requirements, and success criteria before using the generated prompt for execution.

Risk: Prompt text that asks for reasoning disclosure may be broader than needed for some deployments.

Mitigation: Replace requests for detailed reasoning with concise rationale or decision summaries where policy or privacy requirements call for less disclosure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flonerze/skills/prompt-improve)
- [Publisher profile](https://clawhub.ai/user/flonerze)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill only returns an optimized prompt; it does not execute the requested task, inspect files, or call tools.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
