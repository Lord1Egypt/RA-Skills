## Description:

Control Nanoleaf light panels via the Picoleaf CLI for power, brightness, RGB/HSL color, and color temperature changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rstierli](https://clawhub.ai/user/rstierli)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure Picoleaf and issue local CLI commands that control Nanoleaf light panels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install options can place an unverified third-party executable on the user's machine.

Mitigation: Review the install path before installing, prefer a verified and pinned Picoleaf source when available, and inspect the Homebrew formula or downloaded archive before use.

Risk: The local Picoleaf configuration stores a reusable Nanoleaf device access token in plaintext.

Mitigation: Create ~/.picoleafrc with owner-only permissions, such as mode 600, and protect it like a credential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rstierli/skills/nanoleaf)
- [Picoleaf GitHub repository](https://github.com/tessro/picoleaf)
- [Picoleaf Linux binary release archive](https://github.com/tessro/picoleaf/releases/latest/download/picoleaf_1.4.0_linux_amd64.tar.gz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Picoleaf CLI, a reachable Nanoleaf controller, and a local access token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
