## Description:

Harness Engineering guides agents that build coding, automation, or long-running harness agents using a loop-plus-rings architecture, design decisions, Python templates, and long-running patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edde-101](https://clawhub.ai/user/edde-101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents when implementing coding, automation, or long-running agent harnesses. It provides architecture, design choices, and reusable templates rather than executing code or modifying projects itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable file and shell templates may be copied into a harness without sufficient execution boundaries.

Mitigation: Add workspace path enforcement, command allowlists or approval prompts, and sandboxing before using the templates in a real agent.

Risk: Session examples persist conversation and tool data as plaintext JSONL, which may expose sensitive information.

Mitigation: Apply secret redaction before persistence, secure session-file permissions, and define retention controls.

Risk: The artifact is guidance and template material, so generated implementations may omit required controls if copied mechanically.

Mitigation: Review generated harness code against the build checklist and security guidance before deployment.

## Reference(s):

- [Agent Harness Architecture](artifact/references/architecture.md)
- [Design Decisions](artifact/references/design-decisions.md)
- [Python Code Templates](artifact/references/code-templates.md)
- [Long-Running Agent Patterns](artifact/references/long-running-patterns.md)
- [Harness Comparison](artifact/references/harness-comparison.md)
- [Server-Resolved Source Repository Path](https://github.com/Edde-101/harness-engineering/tree/main/harness-engineering)
- [ClawHub Skill Page](https://clawhub.ai/edde-101/skills/harness-engineering-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python code blocks, shell command examples, checklists, and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces reference material for an agent to adapt; generated templates require security review and hardening before production reuse.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter version is 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
