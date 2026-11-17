## Description:

Create macOS desktop app launchers for development projects that open Terminal and run a local dev server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create clickable macOS Desktop launchers for local development projects, optionally choosing the app name, start command, icon, and output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent macOS .app launchers that run project commands in Terminal.

Mitigation: Use it only for trusted local projects, and review the generated launcher command before relying on the app bundle.

Risk: The artifact includes an embedded external API credential used for optional icon generation.

Mitigation: Avoid --auto-icon unless that credential has been removed and an approved key is supplied through the environment.

Risk: Unsafe path, app name, or command handling could make generated launcher scripts behave unexpectedly.

Mitigation: Validate project paths, app names, and start commands before generation, especially when values come from an untrusted project.

## Reference(s):

- [Phy App Launcher on ClawHub](https://clawhub.ai/phy041/skills/phy-app-launcher)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [macOS .app bundle with Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent macOS application bundles that run local project commands in Terminal.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
