## Description:

Pi EvoX Loop adds an experience-inheritance runtime for coding agents that recalls validated fixes, records when they help, and saves useful new fixes for future tasks, with optional controlled experiments to measure the effect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stwhwing](https://clawhub.ai/user/stwhwing)

### License/Terms of Use:

MIT

## Use Case:

Developers using coding agents can recall validated fixes at the start of non-trivial tasks, record when a fix helps, and save useful new fixes after resolving a failure. They can also run controlled experiments to measure whether inherited fixes improve repeat tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with medium confidence and reports security and scope concerns. Inspection was partial; the supplied guidance calls out cleanup, approval, network-permission, and dependency concerns for review.

Mitigation: Review those areas and optional dependencies before installation; keep automatic approval off unless deliberately enabled, and review data flows before enabling networked integrations.

Risk: The optional --llm-refine path sends session transcript text to the configured external endpoint.

Mitigation: Keep it disabled unless needed; before enabling it, review the endpoint and the transcript data that will be sent.

Risk: The --fresh option clears the global experience library after creating a backup.

Mitigation: Use it only when a reset is intended and confirm the backup is available before proceeding.

Risk: The optional EvoMap integration is documented as GPL-3.0-or-later, which may affect commercial or closed-source deployments.

Mitigation: Review the dependency's license terms before enabling that integration in a commercial or closed-source environment.

## Reference(s):

- [Pi EvoX Loop on ClawHub](https://clawhub.ai/stwhwing/skills/pi-evox-loop)
- [Pi EvoX Loop project documentation](https://github.com/stwhwing/pi-evox-lab)
- [Security and license notes](artifact/docs/security-and-license.md)
- [Boundaries and trigger guide](artifact/docs/boundary-and-triggers.md)
- [Optional EvoMap evolver integration](https://github.com/EvoMap/evolver)
- [Pi coding agent integration](https://github.com/earendil-works/pi)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance and shell commands, with structured JSON or JSONL records and reports where applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Numbered reusable fixes; Node.js 22 or later is required.]

## Skill Version(s):

0.42.0 (source: server-resolved release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
