## Description:

Redirect users to install `gsd-orchestrator` instead of this name-reservation skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glittercowboy](https://clawhub.ai/user/glittercowboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents encounter this skill as a placeholder for the `gsd-cli` name and are directed to install `gsd-orchestrator` for full GSD orchestration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The visible skill content only redirects to `gsd-orchestrator`, but the release declares an automatic Node package install that is not needed for that placeholder purpose.

Mitigation: Prefer installing the real `gsd-orchestrator` skill directly, or proceed only after separately trusting the `gsd-pi` package and installer behavior.

## Reference(s):

- [GSD CLI on ClawHub](https://clawhub.ai/glittercowboy/skills/gsd-cli)
- [gsd-orchestrator skill](https://clawhub.com/skills/gsd-orchestrator)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Placeholder redirect; declared metadata requires the `gsd` binary and a Node package install for `gsd-pi`.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-03-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
