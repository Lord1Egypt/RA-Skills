## Description:

Install the Mobazha native binary on Linux, macOS, or Windows when the user wants to run a store without Docker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengzie](https://clawhub.ai/user/fengzie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and manage a Mobazha store as a native binary on Linux, macOS, or Windows when Docker is not desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote shell scripts can change between reviews and execute installer behavior on the user's machine.

Mitigation: Review the installer before execution and prefer a signed, versioned release or a downloaded installer with a verifiable checksum or signature.

Risk: The installer can auto-start services and install auto-update components.

Mitigation: Use --no-start for initial installation when available, then inspect the installed service and auto-update behavior before enabling it.

Risk: Purge operations can remove local store data.

Mitigation: Back up store data before any purge operation.

## Reference(s):

- [Mobazha Self-Host Guide](https://mobazha.org/self-host)
- [Mobazha Downloads](https://mobazha.org/download)
- [Native Install on ClawHub](https://clawhub.ai/fengzie/skills/mobazha-native-install)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes install, service management, backup, uninstall, and troubleshooting guidance.]

## Skill Version(s):

0.2.0 (source: server release evidence, released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
