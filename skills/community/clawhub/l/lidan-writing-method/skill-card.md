## Description:

This skill guides agents to write smooth Chinese explanatory articles using a seven-step internal framework for explaining complex concepts in philosophy, business, AI, linguistics, and sociology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyischen](https://clawhub.ai/user/whyischen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to draft Chinese long-form explanatory articles that make complex concepts easier to understand and retell. It is best suited for conceptual education, essays, and deep explanations rather than short notices, news updates, or technical documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can impose a specific Chinese long-form style on tasks where the user asked for a different language, tone, or short answer.

Mitigation: Enable it only for matching Chinese long-form explanatory writing, and let explicit user requirements for tone, language, and brevity take priority.

Risk: The framework asks for data comparisons and reading recommendations, which may introduce unsupported facts if drafted without source checks.

Mitigation: Review factual claims, data comparisons, and book recommendations before publication.

Risk: The optional article checker is heuristic and does not establish factual accuracy or overall suitability.

Mitigation: Use the checker as a drafting aid, then manually review the article for correctness, audience fit, and quality.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whyischen/skills/lidan-writing-method)
- [Publisher profile](https://clawhub.ai/user/whyischen)
- [Quality checker guide](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Chinese prose in Markdown, with optional quality-check report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Framework titles should be hidden in final articles; the optional checker reads a local article file and prints pass/fail suggestions.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
