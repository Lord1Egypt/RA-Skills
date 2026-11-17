## Description:

Applies an inversion audit to high-stakes plans by working backward from failure, ranking failure paths, and designing mitigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Decision-makers and teams use this skill to stress-test high-stakes or hard-to-reverse plans, prioritize load-bearing failure paths, and define mitigations, not-to-do rules, and abort triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to fetch changeable online instructions each run; remote revisions may differ from the reviewed local copy.

Mitigation: Prefer a reviewed local copy with the runtime fetch disabled, or review remote revisions before adopting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deciqai/skills/inversion)
- [deciqAI current skill instructions](https://www.deciqai.com/s/inversion.json)
- [Source list](references/sources.md)
- [Performing a Project Premortem (Harvard Business Review)](https://hbr.org/2007/09/performing-a-project-premortem)
- [Apollo 204 Review Board Final Report](https://history.nasa.gov/Apollo204/)
- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown inversion audit with ranked failure paths, mitigation actions, not-to-do rules, and an abort trigger.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a concrete decision and adequate domain knowledge; not intended for immediate crisis response or low-stakes reversible choices.]

## Skill Version(s):

1.0.8 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
