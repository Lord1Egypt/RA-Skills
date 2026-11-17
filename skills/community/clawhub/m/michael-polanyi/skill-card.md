## Description:

Helps agents rewrite generic advice into grounded practitioner judgment for ambiguous decisions, critiques, trade-offs, and incomplete information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[august1314](https://clawhub.ai/user/august1314)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and team leads use this skill when advice, strategy, critique, or decision-making responses are technically plausible but too generic. It guides the agent to state a clear judgment, surface practical signals, name trade-offs and boundaries, and end with one concrete next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decisive guidance can be misleading if the agent overstates a judgment under incomplete information.

Mitigation: Require visible facts, assumptions, boundaries, and flip conditions before acting on the recommendation.

Risk: The skill can drift into unsupported intuition, pseudo-depth, or generic advice if its response contract is applied loosely.

Mitigation: Use the provided quality checks and optional scanner to catch empty balance, pseudo-depth, and unsubstantiated confidence.

Risk: The optional checker script scans text files supplied by the user.

Mitigation: Run the checker only on text intentionally selected for local scanning, especially when drafts may contain sensitive information.

## Reference(s):

- [Polanyi Concept Reference](polanyi-notes.md)
- [Response Patterns](references/response-patterns.md)
- [Quality Checks](references/quality-checks.md)
- [Anti-Generic Advice Detection](references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional shell commands or JSON scanner reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish facts, interpretations, and hypotheses, state boundaries, and include one concrete next step.]

## Skill Version(s):

0.5.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
