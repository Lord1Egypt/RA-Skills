## Description:

17TRACK (17track.net). Use this skill for ANY 17TRACK request — reading, creating, and updating data. Whenever a task involves 17TRACK, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected 17TRACK account use this skill to check tracking quotas, list and inspect shipments, and register tracking numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute remote code without a clear approval step.

Mitigation: Review and install a specific CLI release yourself, require approval for setup changes, and check the CLI's automatic skill-synchronization settings.

Risk: Registering tracking numbers changes the connected 17TRACK account.

Mitigation: Connect only the intended 17TRACK account and confirm the exact registration payload and effect with the user before running it.

## Reference(s):

- [17TRACK](https://www.17track.net/)
- [17TRACK API Documentation](https://api.17track.net/en/doc)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and JSON tracking data, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shipment registration changes account data and requires user confirmation.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
