## Description:

PinchTab Helper helps agents control a local PinchTab browser service for navigation, page snapshots, clicking, form filling, form submission, and screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to automate browser workflows through PinchTab after installing and starting its local service. It is suited for web navigation, search, interaction with page elements, snapshots, and screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-impact browser control through a local service with weak safeguards.

Mitigation: Review the skill before installing, use a dedicated browser profile, and avoid logged-in or sensitive sites unless the PinchTab service is trusted.

Risk: Remote or non-local exposure of the browser-control service could allow unintended browser actions.

Mitigation: Keep the service bound to localhost unless there is a clear token and network exposure plan, and configure BRIDGE_TOKEN for remote access.

Risk: Installer commands can execute code from external package or script sources.

Mitigation: Prefer pinned and verifiable installation methods before running PinchTab installation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adminlove520/skills/pinchtab-helper)
- [Publisher profile](https://clawhub.ai/user/adminlove520)
- [PinchTab install script](https://pinchtab.com/install.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples and HTTP endpoint summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed and running local PinchTab service before browser-control commands can be used.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
