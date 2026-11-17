## Description:

Handle Clawdbot operations in Nix mode (configuration management, environment detection).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chronicuser21](https://clawhub.ai/user/chronicuser21)

### License/Terms of Use:


## Use Case:

Developers and agents operating Clawdbot in Nix-managed environments use this skill to detect Nix mode, avoid unsupported auto-install flows, and provide configuration and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could attempt auto-installation or self-modification even though Nix-managed installations are intended to be immutable.

Mitigation: Respect Nix mode, avoid auto-install flows, and direct dependency changes through Nix package management.

Risk: Incorrect Nix environment or path handling could lead to misleading configuration guidance.

Mitigation: Check CLAWDBOT_NIX_MODE and distinguish Nix store, configuration, and state paths before advising remediation.

## Reference(s):

- [Nix Mode ClawHub Skill Page](https://clawhub.ai/chronicuser21/skills/nix-mode)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown guidance with inline environment variable and path names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
