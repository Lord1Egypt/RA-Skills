## Description:

Md Viewer helps an agent provide a LAN-accessible browser viewer for local Markdown files, optimized for comfortable reading on e-readers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoangcongst](https://clawhub.ai/user/hoangcongst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to provide a browser link for viewing a local Markdown file directly, including from another device on the same trusted Wi-Fi network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Markdown files may be exposed over the network by default.

Mitigation: Use only on trusted networks and prefer --localhost unless LAN sharing is required.

Risk: Reusable token URLs and long-lived cookies can grant continued access if shared too broadly.

Mitigation: Do not distribute token URLs beyond intended viewers, and restart the server or use a new password when access should be revoked.

Risk: Viewed file paths are persisted in history by default.

Mitigation: Use --no-history for private files or when retaining local path history is undesirable.

Risk: Security evidence flags unresolved authentication and path-validation concerns.

Mitigation: Review before installing and avoid opening sensitive Markdown files until those issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hoangcongst/skills/md-viewer)
- [Python-Markdown](https://github.com/Python-Markdown/markdown)
- [Bleach](https://github.com/mozilla/bleach)
- [highlight.js](https://highlightjs.org/)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [shell commands, text, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local or LAN URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a local HTTP server, generates password-protected Markdown viewer links, and may write local history unless disabled.]

## Skill Version(s):

1.0.2 (source: VERSION.md, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
