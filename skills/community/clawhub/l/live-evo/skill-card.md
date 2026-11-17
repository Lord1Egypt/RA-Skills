## Description:

Self-evolving memory system that learns from verifiable tasks, retrieves relevant past experiences, and generates task-specific guidelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mercury7353](https://clawhub.ai/user/mercury7353)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve and apply lessons from previous verifiable tasks, including coding, analysis, predictions, debugging, and problem solving. It supports feedback-driven learning by storing task outcomes and updating experience weights when usefulness can be assessed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory may retain sensitive task content in ~/.live-evo and later surface it as guidance.

Mitigation: Avoid storing secrets, proprietary code, personal data, incident details, or other sensitive content; add consent, redaction, and deletion controls before broader use.

Risk: User feedback or task text stored as experience data can become future guidance without strong prompt-injection handling.

Mitigation: Review retrieved guidance before applying it and treat stored experiences from untrusted inputs as untrusted content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mercury7353/skills/live-evo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSONL-backed local experience records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval and management scripts read and write persistent local experience data under ~/.live-evo.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
