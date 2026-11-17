## Description:

Connect and control Midea devices through the Midea cloud with a local cached account and device configuration for account setup, device listing, and air-conditioner power on/off commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fooklook](https://clawhub.ai/user/fooklook)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Midea cloud accounts use this skill to connect their account, cache discovered Midea device metadata locally, list devices, and send cloud power on/off commands to named Midea air conditioners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the user's Midea account password in a local JSON configuration file.

Mitigation: Warn before first-time credential storage, avoid echoing passwords, restrict file permissions where possible, and prefer an OS credential manager in a hardened version.

Risk: The setup command passes the Midea password through a command-line argument that may be visible to local process observers.

Mitigation: Prefer prompting through stdin or another non-argument secret path, and avoid running the command on shared or untrusted systems.

Risk: Cloud write calls may report success before physical device behavior is confirmed.

Mitigation: Report only that the cloud command was sent and ask the user to confirm the device reacted before treating the physical state as changed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fooklook/skills/midea-cloud-control)
- [API Notes](references/api-notes.md)
- [Generated Config Store](references/generated-config-store.md)
- [Generated Midea Skill CLI](references/generated-midea-skill-cli.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local Python helper files on first use and returns command results as JSON summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
