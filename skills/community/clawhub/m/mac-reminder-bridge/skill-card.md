## Description:

Manage macOS Reminders.app from Docker through an HTTP bridge for creating, listing, updating, completing, and deleting reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masteryuuuu](https://clawhub.ai/user/masteryuuuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to let a containerized agent operate a local macOS Reminders.app bridge. It is intended for reminder CRUD workflows such as adding, listing, editing, completing, reopening, and deleting reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge can read, edit, complete, and delete real macOS Reminders data.

Mitigation: Run it only on a trusted local Mac, confirm Reminders permission prompts intentionally, and use DRY_RUN for testing when changes should not be written.

Risk: The default HTTP bridge security is too broad for real reminder data and update or deletion authority.

Mitigation: Set a strong BRIDGE_SECRET, keep BRIDGE_ALLOWED_IPS narrowed to the exact client or Docker subnet, and avoid exposing port 5000 to remote networks.

Risk: Direct HTTP cloud access can expose reminder operations outside the local trust boundary.

Mitigation: Do not use direct HTTP for cloud access; place any remote access behind an authenticated and encrypted channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/masteryuuuu/skills/mac-reminder-bridge)
- [ClawHub publisher profile](https://clawhub.ai/user/masteryuuuu)
- [macOS platform](https://www.apple.com/macos/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with JSON request bodies and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent actions target HTTP JSON endpoints exposed by a local macOS listener.]

## Skill Version(s):

2.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
