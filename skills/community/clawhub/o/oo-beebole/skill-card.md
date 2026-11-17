## Description:

Beebole (beebole.com). Use this skill for ANY Beebole request — reading, creating, and updating data. Whenever a task involves Beebole, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Beebole account users can read and manage their Beebole data through an OOMOL-connected account. The skill guides the agent to inspect action schemas, submit connector requests, and confirm changes before write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup can run unverified remote installation code without a separate approval step.

Mitigation: Prefer a reviewed, version-pinned CLI; require approval before local installation; and review or disable automatic skill synchronization.

Risk: Beebole write actions can change account data.

Mitigation: Confirm the exact payload and effect before write actions, and explicitly confirm the target of destructive actions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-beebole)
- [Beebole API documentation](https://beebole.com/help/api/introduction)
- [Beebole homepage](https://beebole.com)
- [oo CLI project (referenced by the skill)](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector requests and results, with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change Beebole data require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
