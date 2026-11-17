## Description:

Perplexity Sonar search and answer generation through AIsa. Use when the task is specifically to call Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, or Sonar Deep Research for citation-backed web answers, analytical reasoning, or long-form research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renning22](https://clawhub.ai/user/renning22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need Perplexity-backed web answers, reasoning, or research reports through AIsa Sonar endpoints with citation-oriented output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to AIsa Perplexity-backed external services and may include user-provided context.

Mitigation: Avoid sending secrets, confidential documents, regulated data, or private internal context unless that external processing is acceptable for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renning22/skills/my-perplexity-search)
- [OpenClaw](https://openclaw.ai)
- [AIsa Sonar API reference](https://docs.aisa.one/reference/post_perplexity-sonar)
- [AIsa Sonar Pro API reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro)
- [AIsa Sonar Reasoning Pro API reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro)
- [AIsa Sonar Deep Research API reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends prompts to AIsa Perplexity-backed endpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
