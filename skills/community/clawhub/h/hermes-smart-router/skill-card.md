## Description:

Use when switching models, saving costs, or routing queries; it classifies requests locally and recommends the cheapest model tier that can handle the task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydatalab](https://clawhub.ai/user/raydatalab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide when to keep work on local or lower-cost models and when to recommend a higher-capability tier for complex reasoning, architecture, debugging, or multi-step coding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad routing-related phrases may activate the skill in model-selection or cost-saving conversations where routing is not desired.

Mitigation: Review routing recommendations before switching tiers and skip routing for greetings, simple translations, one-line factual requests, and very short prompts.

Risk: Using the router backend may require a local Ollama service or model download before routing works.

Mitigation: Confirm Ollama and required local models are installed before relying on routing; if a router call fails or times out, continue without retrying.

Risk: Short prompts can bypass routing even when they need a stronger model tier.

Mitigation: Use manual tier or model selection for short prompts that still require complex reasoning or advanced coding support.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raydatalab/skills/hermes-smart-router)
- [Hermes Smart Router Homepage](https://github.com/raydatalab/hermes-smart-router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing recommendations and setup guidance; no API keys are required for local routing classification.]

## Skill Version(s):

0.2.2 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
