## Description:

Operate Fluxguard through an OOMOL-connected account for reading, creating, updating, and deleting Fluxguard data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect and manage monitored Fluxguard pages, initiate crawls, and manage categories and webhooks through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs remote installer code that was unavailable for inspection and may introduce persistent changes to agent skills through automatic synchronization.

Mitigation: Review and approve CLI installation separately before fallback setup, understand that Fluxguard requests pass through OOMOL, and review or disable automatic skill synchronization if unwanted.

## Reference(s):

- [Fluxguard homepage](https://fluxguard.com/)
- [Fluxguard API documentation](https://fluxguard.com/how-to-guides/use-our-api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Fluxguard ClawHub release](https://clawhub.ai/oomol/skills/oo-fluxguard)

## Skill Output:

**Output Type(s):** [Shell commands, JSON]

**Output Format:** [oo CLI commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require confirmation; destructive actions remove or overwrite data.]

## Skill Version(s):

1.0.5 (source: artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
