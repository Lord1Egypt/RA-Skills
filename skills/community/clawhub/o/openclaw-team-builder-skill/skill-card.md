## Description:

Composes specialist teams from OpenClaw core agents, Agency division specialists, and a research loop, with planner-generated rosters and reviewer quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeszeles](https://clawhub.ai/user/joeszeles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to classify incoming work, assemble an appropriate multi-agent team, define activation order and handoffs, and require evidence-based review before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates work to external agent definition files that may be missing or untrusted.

Mitigation: Use only bundled or allowlisted agent definitions, and verify each specialist definition before activation.

Risk: Trading workflows can propose strategy changes that may affect live market activity.

Mitigation: Keep trading changes read-only or sandboxed by default and require explicit human approval before deployment or trade-related actions.

Risk: Autonomous experiment loops can continue indefinitely or over-optimize without sufficient controls.

Mitigation: Set fixed budgets, stop conditions, experiment ledgers, and review gates before running iterative optimization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeszeles/skills/openclaw-team-builder-skill)
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch)
- [SKILL.md](artifact/SKILL.md)
- [PLANNER.md](artifact/PLANNER.md)
- [REVIEWER.md](artifact/REVIEWER.md)
- [TEAM-RESEARCH.md](artifact/TEAM-RESEARCH.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown team proposals, handoff plans, review checklists, and experiment ledgers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed agent rosters, activation phases, acceptance criteria, risks, and validation evidence requirements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
