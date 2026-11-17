## Description:

OpenClaw-chat is a mobile app for managing multi-agent chats, groups, service controls, scheduled tasks, and logs with Android, iOS, and PWA packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsun4414](https://clawhub.ai/user/johnsun4414)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to package and run a mobile-oriented OpenClaw administration interface for agent chat, group views, service status, cron views, logs, and emergency controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package claims high-impact remote management, repair, restore, and service-control capabilities that are not safely scoped or fully implemented in the packaged artifact.

Mitigation: Treat the release as a prototype or mock administration UI until the publisher supplies a real authenticated backend and clear controls for memory sync, destructive actions, and dependency updates.

Risk: Users could mistake the emergency, cron, stop/start, restore, or self-healing screens for reliable operational controls.

Mitigation: Do not rely on these screens for real operations without independent validation, access control review, and end-to-end testing against the intended backend.

## Reference(s):

- [Openclaw Chat on ClawHub](https://clawhub.ai/johnsun4414/skills/openclaw-chat)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [React/TypeScript app files with Markdown setup and build instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes PWA assets plus Android and iOS Capacitor project files.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
