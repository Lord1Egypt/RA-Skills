## Description:

Meta Formal Capability Contract is a distilled meta-skill for applying formal capability-contract workflows with added self-verification, reflection, adversarial checks, and learner-backed iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to guide formal precondition, postcondition, and invariant checks while adding self-verification and reflection around each output. It is intended for agent workflows that need traceable contract-style reasoning and iterative reliability review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to persist and reuse learner notes across sessions, which can carry untrusted or stale context into later work.

Mitigation: Keep learner notes inspectable and resettable, treat saved notes as untrusted data, and require explicit review before using them in future planning or memory.

Risk: The skill joins broader agent control loops, so mistakes in self-verification or reflection could influence multi-step execution.

Mitigation: Review generated plans and scans before deployment, and keep verification and reflection outputs advisory unless a human approves their use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-formal-capability-contract)
- [Publisher profile](https://clawhub.ai/user/qq435912743)
- [Skill definition](artifact/SKILL.md)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text with optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May record learner notes in a local JSON file when its learner script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
