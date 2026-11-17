## Description:

Designs a gated, machine-checkable Codex CLI loop for a medium or large AI-coding task and produces a runnable runbook without executing it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and document bounded, test-gated Codex CLI coding workflows for review before anyone runs them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated runbooks can drive autonomous code changes if executed without review.

Mitigation: Review the generated .loop files and approve the proposed checks, scope, and stopping conditions before running them.

Risk: A known contract-protection gap can allow unsafe designs to pass the skill's checks.

Mitigation: Before evaluator launches, keep contract.md, AGENTS*/AGENTS.override.md, .codex/, .rules, and .loop/prompts outside the generator's write surface or verify their hashes; do not treat a clean lint and fresh-reader pass as proof of this boundary.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vincentjiang06/skills/loop-constructor-codex)
- [Loop selection procedure](artifact/references/loop-selection.md)
- [Codex runtime guidance](artifact/references/codex-runtime.md)
- [Loop design format](artifact/references/loop-design-shape.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Machine-checkable loop design JSON and Markdown .loop/ runbook with a decision log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Design-only; the skill does not execute the proposed loop.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
