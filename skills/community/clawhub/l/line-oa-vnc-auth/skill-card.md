## Description:

Use when LINE Official Account access requires a user-operated temporary VNC/noVNC login, MFA/QR completion, session verification, and secure teardown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosluce](https://clawhub.ai/user/mosluce)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing a LINE Official Account use this skill when a user must complete LINE Business ID login, MFA, or QR verification in a temporary remote browser before the agent verifies the session and sends an approved message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow exposes a live LINE Official Account session through a public Cloudflare Quick Tunnel.

Mitigation: Use the tunnel only for authorized LINE OA work, protect noVNC with a high-entropy short-lived VNC password, and close the tunnel as soon as login or verification is complete.

Risk: The documented Chromium command disables sandboxing and may retain an authenticated browser profile.

Mitigation: Run inside a disposable VM, container, or dedicated unprivileged user account, avoid --no-sandbox when the host supports sandboxing, and delete the isolated browser profile unless the user explicitly requests retention.

Risk: Temporary screenshots, VNC password files, and access artifacts can contain private chat or authentication material.

Mitigation: Delete VNC plaintext and hash files, temporary screenshots, QR artifacts, and other remote-access files during teardown.

## Reference(s):

- [Source repository](https://github.com/mosluce/line-oa-vnc-auth)
- [ClawHub skill page](https://clawhub.ai/mosluce/skills/line-oa-vnc-auth)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and verification checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for temporary remote browser access, login verification, message sending, and teardown.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
