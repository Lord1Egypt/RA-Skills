## Description:

Redirect users to install `gsd-orchestrator` instead of this name-reservation skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glittercowboy](https://clawhub.ai/user/glittercowboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents encountering `gsd-agent` use it as a redirect to the full `gsd-orchestrator` skill for GSD subprocess orchestration patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing this redirect skill may unnecessarily install the unpinned `gsd-pi` Node package.

Mitigation: Prefer installing `gsd-orchestrator` directly unless the publisher and `gsd-pi` package are specifically trusted and needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glittercowboy/skills/gsd-agent)
- [gsd-orchestrator skill](https://clawhub.com/skills/gsd-orchestrator)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redirect guidance only; no structured runtime output is defined.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
