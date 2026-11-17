## Description:

Meta Agent Eval Harness is a distilled enhancement of agent-eval-harness that adds self-verification, self-reflection, super-agent orchestration, and a continuous self-improvement loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to define evaluation cases, run regression-style checks, review failures, and improve agent workflows through self-verification and reflection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user preferences, failure notes, and learned patterns across sessions.

Mitigation: Use it in a contained, single-user setting and avoid recording secrets or sensitive personal data.

Risk: The skill describes self-improvement behavior that may rewrite its own instructions.

Mitigation: Require human review before any automatic edits to SKILL.md or other instruction files are accepted.

Risk: Security evidence classifies the release as suspicious because persistence and self-editing controls are unclear.

Mitigation: Review the skill carefully before installation and scan changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-agent-eval-harness)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON learner records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May record usage outcomes, failure notes, and learned patterns when the learner script is invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
