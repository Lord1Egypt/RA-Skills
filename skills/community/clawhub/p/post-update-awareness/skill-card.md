## Description:

After an OpenClaw version change, this skill reads the CHANGELOG entry pinned to the installed version and surfaces user-relevant changes, breaking changes, and optional native dependencies that may need verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hussein1362](https://clawhub.ai/user/hussein1362)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill after an update to detect version changes, summarize pinned release notes, and flag plugin drift, channel health, optional dependency, or config warnings without performing maintenance actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw version, plugin, channel, update-guard, and per-profile state information.

Mitigation: Install it only where those local operational signals are appropriate to inspect, and keep surfaced output limited to update-relevant diagnostics.

Risk: The skill may make unauthenticated GitHub requests for pinned release notes when no local changelog is available.

Mitigation: Prefer the local changelog when present and request only the exact installed version tag; offline environments should expect the no-notes fallback.

Risk: The skill may identify plugin drift, stale config entries, missing optional dependencies, or unhealthy channels but is not scoped to fix them.

Mitigation: Leave updates, config edits, dependency installs, and restarts to the user or the separate post-update-maintenance skill.

Risk: Writing notification state too early could suppress future update notices.

Mitigation: Persist the per-profile state file only after the update notice has been successfully surfaced and acknowledged.

## Reference(s):

- [Post Update Awareness on ClawHub](https://clawhub.ai/hussein1362/skills/post-update-awareness)
- [OpenClaw versioned CHANGELOG](https://github.com/openclaw/openclaw/blob/v<newVersion>/CHANGELOG.md)
- [Post Update Maintenance companion skill](https://clawhub.ai/skills/post-update-maintenance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Concise Markdown notice with short bullet buckets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caps the surfaced notice at about 18 lines and writes per-profile state only after successful surfacing.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
