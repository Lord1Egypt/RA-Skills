## Description:

Redirect users to install `gsd-orchestrator` instead of this name-reservation skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glittercowboy](https://clawhub.ai/user/glittercowboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a redirect when they encounter the reserved `gsd-pi` name and need the functional `gsd-orchestrator` skill for GSD subprocess orchestration patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation metadata may fetch and install the external Node package `gsd-pi`, even though the artifact content is only a redirect.

Mitigation: Review the package before installation and prefer installing `gsd-orchestrator` directly unless the reserved package is specifically trusted and needed.

## Reference(s):

- [GSD Orchestrator Skill](https://clawhub.com/skills/gsd-orchestrator)
- [GSD Pi ClawHub Skill Page](https://clawhub.ai/glittercowboy/skills/gsd-pi)
- [glittercowboy Publisher Profile](https://clawhub.ai/user/glittercowboy)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Name-reservation redirect; no substantive orchestration workflow is provided by this skill.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
