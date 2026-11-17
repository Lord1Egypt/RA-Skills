## Description:

Long-term verification agents for the PASM cognitive engine that run repeatable checks for memory retention, salience-aware eviction, emotion drift, behavioural entropy collapse, persona saturation, forgetting curve behavior, 6000-step soak degradation, and cross-repo parity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run PASM long-run verification agents, archive JSON findings, compare baselines, and identify regressions or durability issues in cognitive engine behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install PASM packages or clone related repositories before running verification commands.

Mitigation: Install only when PASM verification tooling is intended, and review package and repository sources before executing commands.

Risk: Most operational documentation is written in Chinese, which can lead to misunderstood setup, result interpretation, or baseline update steps.

Mitigation: Translate or review the documentation with a Chinese reader before running commands in an environment where results matter.

Risk: Baseline update commands can make the current system state the comparison baseline.

Mitigation: Run baseline updates only after confirming the current PASM state is correct and suitable as the future comparison point.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arronjack/skills/pasm-longterm-verify)
- [pasm-agents source repository](https://github.com/arronJack/pasm-agents)
- [pasm-skills base repository](https://github.com/arronJack/pasm-skills)
- [pasm-skills tutorial](https://github.com/arronJack/pasm-skills/blob/master/docs/TUTORIAL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, configuration examples, and JSON reporting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification runs can emit JSON-archivable and baseline-diffable findings.]

## Skill Version(s):

0.5.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
