## Description:

App Store Connect (appstoreconnect.apple.com). Use this skill for ANY App Store Connect request — reading, creating, updating, and deleting data. Whenever a task involves App Store Connect, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

App developers and release teams use this skill to read and manage App Store Connect resources, including app metadata, TestFlight, releases, and related account records, through OOMOL's oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs remote installers whose exact effects are unverified.

Mitigation: Review and install a verified, pinned CLI release separately before use.

Risk: Setup may make broader agent-skill changes without explaining them.

Mitigation: Consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1 and review skill changes.

Risk: App Store Connect write actions can change or remove account and app records.

Mitigation: Keep approval requirements for changes and inspect the action schema and exact payload before execution.

## Reference(s):

- [App Store Connect](https://appstoreconnect.apple.com/)
- [App Store Connect API documentation](https://developer.apple.com/documentation/appstoreconnectapi)
- [oo CLI repository (referenced by the skill)](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-app-store-connect)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change App Store Connect records; write and destructive actions require approval.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
