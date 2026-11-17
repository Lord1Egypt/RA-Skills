## Description:

Minimize user friction by asking up to 4 clarifying questions before executing actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szpili](https://clawhub.ai/user/szpili)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to have an agent resolve ambiguous requests with a small number of clarifying questions before taking action. It is most relevant before high-impact actions, incomplete requests, and workflows that require assumptions to be summarized before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A request may remain ambiguous after the configured question limit.

Mitigation: Summarize the understood task, list assumptions, and ask for confirmation when the action is high risk.

Risk: The examples are in Polish and could be mistaken for a language requirement.

Mitigation: Treat the examples as illustrative only and preserve the user's preferred language.

## Reference(s):

- [Guided Conversation ClawHub Skill](https://clawhub.ai/szpili/skills/guided-conversation)
- [szpili ClawHub Publisher Profile](https://clawhub.ai/user/szpili)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Natural language with short Markdown lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include up to 4 clarifying questions, a one-sentence task summary, assumptions, and risk-based confirmation prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
