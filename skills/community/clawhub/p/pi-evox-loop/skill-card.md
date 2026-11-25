## Description:

Adds an experience-inheritance workflow for coding agents: recall validated fixes from a gene store, record when they help, and deposit new fixes after non-obvious failures, with optional controlled experiments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stwhwing](https://clawhub.ai/user/stwhwing)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to reuse previously validated coding fixes, record when those fixes help, and add useful repairs for later tasks. It also supports optional controlled experiments that measure whether inherited fixes improve results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because of weaknesses in reusable-guidance validation and approval, alongside installation and experiment-safety concerns.

Mitigation: Before use, review the approval and experiment workflows and retain human review when fixes are added to reusable guidance.

Risk: ClawScan reports a partial scan: 52 of 82 components were fully scanned and 30 were only partially inspected.

Mitigation: Treat the assessment as incomplete and review components that were only partially inspected before installation.

Risk: Setup guidance may replace existing configuration, and an optional coding-agent dependency may not be needed or current.

Mitigation: Inspect setup changes before applying them, and confirm that the optional dependency is needed and updated.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/stwhwing/skills/pi-evox-loop)
- [Project homepage](https://github.com/stwhwing/pi-evox-lab)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Numbered fix guidance, command snippets, configuration examples, and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the available gene store, host configuration, and whether optional experiments are run.]

## Skill Version(s):

0.44.0 (source: artifact frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
