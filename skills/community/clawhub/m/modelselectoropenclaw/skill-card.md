## Description:

Enhances the OpenClaw Control UI chat model picker with a two-column provider/model selector and helps install, verify, repair, or remove the local browser-side patch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pondsi](https://clawhub.ai/user/pondsi)

### License/Terms of Use:

MIT-style with mandatory attribution

## Use Case:

Developers and OpenClaw users use this skill to improve model selection in the Control UI when many providers and models make the native flat picker slow to navigate. It provides installation, verification, repair, and uninstall guidance for the local UI enhancement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation modifies local OpenClaw Control UI files by injecting a script tag into index.html and copying an asset.

Mitigation: Review the PowerShell command before running it, confirm the target Control UI directory, and use the documented -Remove command to uninstall.

Risk: Open tabs may periodically perform same-origin update checks and reload after a patched install.

Mitigation: Expect browser-side same-origin checks for the local app shell, and install only when that reload behavior is acceptable.

Risk: Running the installer against the wrong directory could patch an unintended OpenClaw Control UI copy.

Mitigation: Use the documented -Dist option for non-standard layouts and verify the printed Control UI path before continuing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pondsi/skills/modelselectoropenclaw)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown instructions with PowerShell commands and browser-console verification checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented commands may install or remove a local browser-side JavaScript asset in the OpenClaw Control UI.]

## Skill Version(s):

1.6.0 (source: SKILL.md metadata, CHANGELOG, and server release evidence, released 2026-09-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
