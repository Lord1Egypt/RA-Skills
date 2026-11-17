## Description:

Control Xiaomi Home devices over a local LAN with miiocli, including status checks, power toggles, and MIOT property changes for smart plugs, humidifiers, and rice cookers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiqiezhenxi](https://clawhub.ai/user/yiqiezhenxi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure and run local miiocli commands for Xiaomi Home devices they control, including token-based status checks, power toggles, and MIOT property changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaomi device tokens are credentials and may be exposed if stored in shared files or agent-visible documents.

Mitigation: Keep tokens out of shared repositories and agent-visible documents, prefer a protected local secret store, and rotate any token that may have been exposed.

Risk: The skill can issue commands that turn appliances on or alter operating modes.

Mitigation: Use only with devices the user controls and require explicit confirmation before power or mode changes.

## Reference(s):

- [ClawHub Xiaomi skill page](https://clawhub.ai/yiqiezhenxi/skills/home-xiaomi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires miiocli and Xiaomi device IP/token credentials supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
