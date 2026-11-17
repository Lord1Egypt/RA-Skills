## Description:

Mobile Text Alerts (mobile-text-alerts.com). Use this skill for ANY Mobile Text Alerts request — reading, creating, updating, and deleting data. Whenever a task involves Mobile Text Alerts, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, support, and marketing teams use the skill to look up and search Mobile Text Alerts subscriber records, or create, update, and delete records through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup pipes a remote installer to a shell, and the installer contents are unverified.

Mitigation: Verify the intended CLI release and review the installer before running it; check its automatic agent-skill synchronization settings.

Risk: Creating, updating, or deleting subscribers changes account data.

Mitigation: Review the exact target and payload before write actions, and obtain explicit approval before deleting a subscriber.

## Reference(s):

- [Mobile Text Alerts](https://mobile-text-alerts.com)
- [Mobile Text Alerts API documentation](https://developers.mobile-text-alerts.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text summaries and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected subscriber action.]

## Skill Version(s):

1.0.4 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
