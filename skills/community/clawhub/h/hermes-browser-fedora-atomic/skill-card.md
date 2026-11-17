## Description:

Use when Hermes browser fails on Fedora Atomic / bootc.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose Hermes browser automation failures on Fedora Atomic or bootc systems and apply a durable local Chromium configuration. It helps distinguish gateway entitlement, real-profile, SPA extraction, and browser_exec issues before changing browser settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx commands download and run the current agent-browser package from npm and install a persistent local Chromium.

Mitigation: Use a pinned, reviewed package version when stronger supply-chain controls are required.

Risk: Layering packages on Fedora Atomic can modify the host image if used broadly.

Mitigation: Use sudo rpm-ostree install <lib> only for a specific missing library that has been verified.

Risk: Leaving browser_exec pointed at a static CDP endpoint can produce reboot-fragile failures.

Mitigation: Prefer Hermes local browser mode for built-in browser tools and verify behavior with agent-browser read and close commands.

## Reference(s):

- [Commands & Config Reference](references/commands-and-config.md)
- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/hermes-browser-fedora-atomic)
- [Project homepage](https://github.com/mina-atef-00/agent-skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Troubleshooting steps for Linux Fedora Atomic / bootc environments]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
