## Description:

Self-improvement layer with evaluation separation, rollback, and tiered operator gates that observes outcomes across sessions, detects recurring patterns, proposes improvements, validates proposals through a separate evaluator invocation, and applies changes with snapshot and rollback capability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to observe recurring agent failures, evaluate proposed improvements through a separate gate, and safely apply or queue persistent memory and instruction updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic observation can retain snippets of tool inputs and error output in .reflect state, which may include sensitive project context.

Mitigation: Use the skill only in trusted workspaces, inspect or clear .reflect state regularly, and avoid external evaluator API keys on sensitive repositories.

Risk: Approved proposals can create persistent changes in MEMORY.md or CLAUDE.md, so manipulated or low-quality observations could make incorrect guidance durable.

Mitigation: Require manual review for MEMORY.md and CLAUDE.md changes, keep high-blast-radius changes operator-gated, and use status and rollback commands to audit or revert applied changes.

Risk: The optional x402 contribution flow can allow autonomous payment activity when an agent has payment capability.

Mitigation: Allow payments only under an explicit operator-controlled policy and review contribution requests before settlement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atlaspa/skills/openclaw-reflect)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Voluntary Contribution Details](AGENT-PAYMENTS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, CLI-style status text, and JSON state records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update .reflect state and append approved learnings to workspace memory or instruction files after evaluation and gating.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
