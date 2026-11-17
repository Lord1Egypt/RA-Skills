## Description:

Sleep helps an OpenClaw agent pause a session by saving unfinished work to a preview file, resetting the session, and restoring that context when the agent resumes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to preserve unresolved tasks across session resets. It is intended for sessions where an agent needs to stop, record pending work, and continue from that saved context later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a shared persistent hook that can affect session bootstrap behavior.

Mitigation: Install and enable the hook only when session sleep/resume behavior is intentionally desired, and remove or disable it when no longer needed.

Risk: The workflow resets sessions and can interrupt the wrong session if the session key is mishandled.

Mitigation: Confirm the current session key before reset and scope use to the intended agent session.

Risk: Preview files may contain detailed task context in plaintext.

Mitigation: Avoid storing secrets or personal data in previews and restrict file permissions for the preview directory.

Risk: The reset flow reads and uses a local gateway token.

Mitigation: Limit installation to trusted environments and review token handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/openclaw-sleep)
- [Publisher profile](https://clawhub.ai/user/axelhu)
- [OpenClaw hook documentation](https://docs.openclaw.ai/automation/hooks)
- [Implementation guide](references/implementation.md)
- [Hook template](references/hook-template/HOOK.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown preview and recovery text with inline shell commands and hook configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-session plaintext preview files and injects pending-work recovery text during agent bootstrap.]

## Skill Version(s):

1.7.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
