## Description:

Access Nylas grants, calendars, and events through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve grant, calendar, and event information from an already connected Nylas account. It guides an agent to inspect an action's schema and submit a matching read request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup runs remote installer code whose behavior and broader installation effects are not verified in the supplied artifact.

Mitigation: Review and verify the installer and its side effects before allowing automatic setup.

Risk: The Nylas connection's permissions and server-side credential handling are not verified by the supplied artifact.

Mitigation: Connect only the intended Nylas account and grant only necessary permissions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-nylas)
- [Nylas API v3 documentation](https://developer.nylas.com/docs/api/v3/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Shell commands and structured JSON connector results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific JSON inputs; connector responses include structured data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
