## Description:

Multi-model peer review layer using local LLMs via Ollama to catch errors in cloud model output and synthesize consensus from multiple critiques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staybased](https://clawhub.ai/user/staybased)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent builders use this skill to review high-stakes model outputs with local Ollama models, aggregate issue flags, and decide whether content should be published, revised, or escalated for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review inputs and outputs may be posted or logged to named Discord channels, which can expose confidential, personal, customer, financial, or unpublished business content.

Mitigation: Keep sensitive content out of this workflow unless Discord posting and logging are disabled, or an explicit approval and redaction process is in place.

Risk: Local model critiques can produce false positives or miss issues, especially for short text, highly technical domains, or time-critical decisions.

Mitigation: Treat consensus as advisory and require human review before publishing or acting on high-stakes conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/staybased/skills/peer-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON issue objects and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Consensus outputs may include issue categories, confidence scores, and publish, revise, or flag_for_human recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter: 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
