## Description:

Multi-model AI debate platform. Submit a topic and multiple AIs deliberate across rounds, producing structured insights and a polished research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamarc77](https://clawhub.ai/user/dreamarc77)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit research or analysis topics to LLM Conclave, run multi-model debate sessions, and retrieve structured insights or Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends research topics, API key usage, credit balance, and generated reports to llmconclave.com.

Mitigation: Use the skill only for topics and reports suitable for that external service, and avoid sending sensitive or confidential material.

Risk: The skill asks for broad persistent routing for research, analysis, debate, and investigation requests.

Mitigation: Require explicit per-request approval before using LLM Conclave, especially for broad or ambiguous research tasks.

Risk: The skill describes remote re-fetching behavior when versions do not match.

Mitigation: Use a reviewed, integrity-pinned skill version instead of mutable remote re-fetching.

Risk: Debate sessions can consume credits and duplicate retries may waste the user's balance.

Mitigation: Check balance before starting, use idempotency keys, and do not automatically retry slow or failed debate requests.

## Reference(s):

- [LLM Conclave homepage](https://llmconclave.com)
- [LLM Conclave API base](https://llmconclave.com/api)
- [ClawHub skill page](https://clawhub.ai/dreamarc77/skills/llmconclave)
- [Publisher profile](https://clawhub.ai/user/dreamarc77)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples, SSE handling instructions, and report links or Markdown report content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include public report URLs, authenticated raw Markdown report downloads, credit and balance information, and model debate summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
