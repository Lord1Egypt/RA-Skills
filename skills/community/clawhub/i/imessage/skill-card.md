## Description:

Enables an OpenClaw agent on macOS to send iMessage texts and images, read recent Messages conversations and contacts, and optionally process admin-only remote-control commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users on macOS use this skill to automate iMessage sending, inspect recent local Messages conversations and contacts, and manage trusted contacts or admin-only remote control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access the local macOS Messages database and send iMessages or SMS messages.

Mitigation: Install only if comfortable granting local Messages and Accessibility access; configure trusted contacts carefully, keep logging enabled, and review message-sending behavior before use.

Risk: Optional remote control can process incoming iMessages from admin contacts and run allowed OpenClaw or ClawHub commands.

Mitigation: Keep remote control disabled unless needed, restrict admin_contacts to specific trusted contacts, keep allowed_commands narrow, and monitor control logs.

Risk: The security guidance flags weaknesses around force=true, AppleScript argument escaping, replay protection, pinned npx usage, and warnings before remote command handling.

Mitigation: Prefer a release that addresses these issues before enabling remote command handling, and do not rely on force=true as a primary safety control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/imessage)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON command results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Messages.app, iMessage sign-in, and local Accessibility or Messages permissions.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
