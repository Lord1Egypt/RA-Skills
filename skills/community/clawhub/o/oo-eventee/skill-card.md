## Description:

Search and read event content, attendee groups, participants, registrations, and session reviews from a connected Eventee account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External Eventee users and developers can retrieve event schedules and related attendee information through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper software may make broader, persistent changes to other agents’ skills, and its remote installers could not be inspected.

Mitigation: Review installation effects, install a verified oo CLI release, and set OO_SKILLS_SYNC_DISABLED=1 for its invocations to prevent startup changes to other agents’ skills. Connect only the intended Eventee account and consider the attendee information it exposes.

## Reference(s):

- [Eventee homepage](https://eventee.co)
- [Eventee API documentation](https://docs.eventee.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-eventee)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Eventee data returned as JSON, with concise natural-language guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only event data; may include attendee information]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
