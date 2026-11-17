## Description:

Redirect skill that reserves the gsd-headless name and directs users to install gsd-orchestrator for full GSD orchestration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glittercowboy](https://clawhub.ai/user/glittercowboy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and ClawHub users encounter this redirect/name-reservation skill when searching for gsd-headless; it points them to install gsd-orchestrator for full GSD headless orchestration patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing this redirect skill can also pull an unpinned Node package, gsd-pi.

Mitigation: Install gsd-orchestrator directly, or review and pin or verify the gsd-pi dependency before using this package.

Risk: The package is redirect-only and does not include the full orchestration workflow users may expect from gsd-headless.

Mitigation: Treat it as a name-reservation pointer and use gsd-orchestrator for subprocess orchestration, status polling, budget handling, and JSON parsing guidance.

## Reference(s):

- [GSD Headless ClawHub release](https://clawhub.ai/glittercowboy/skills/gsd-headless)
- [gsd-orchestrator skill](https://clawhub.com/skills/gsd-orchestrator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redirect-only; no orchestration workflow is included.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
