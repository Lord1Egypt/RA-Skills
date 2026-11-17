## Description:

Check for OpenClaw updates and self-update the installation. Use when the user asks to update OpenClaw, check for updates, upgrade the bot, install a new version, or says a new release is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spideystreet](https://clawhub.ai/user/spideystreet)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to check the installed OpenClaw npm package version, compare it with the latest published version, and apply a user-confirmed update channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or switch the globally installed OpenClaw npm package after confirmation.

Mitigation: Confirm the requested update channel before installation and prefer the stable channel unless beta or dev is intentionally requested.

Risk: An update does not take effect until the OpenClaw gateway is restarted.

Mitigation: After a successful install, restart the gateway manually with the documented OpenClaw restart flow.

Risk: Update checks and installs depend on npm availability and network or npm registry configuration.

Mitigation: Ensure npm is installed and review any npm error output before retrying or changing channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spideystreet/skills/oc-self-update)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command snippets and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports installed and latest OpenClaw versions, asks for confirmation before installing updates, and reminds the user to restart the gateway manually.]

## Skill Version(s):

1.0.2 (source: server release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
