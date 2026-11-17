## Description:

Provides agents on Linux, Windows, or sandboxed environments a prepaid cloud Mac and iOS Simulator for building, testing, signing, and publishing iOS and macOS apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gergomiklos](https://clawhub.ai/user/gergomiklos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software agents use the skill to build and test iOS and macOS apps on a cloud Mac, then manage signing and delivery to TestFlight or the App Store. It also guides project syncing, session use, and credential handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project source and supplied credentials are handled by NoMac, and cloud Macs have broad administrator permissions.

Mitigation: Sync only the intended project, keep unrelated secrets out of the account, and provide required credentials through NoMac's encrypted secret flow.

Risk: The account drive persists after a Mac session stops, so project files may remain in cloud storage.

Mitigation: Download needed work and review or clean the account drive when finished.

## Reference(s):

- [NoMac skill release](https://clawhub.ai/gergomiklos/skills/nomac)
- [NoMac cloud iPhone simulator](https://nomac.app/simulator)
- [NoMac MCP simulator guide](https://mcp.nomac.app/simulator)
- [NoMac hosted MCP endpoint](https://mcp.nomac.app/mcp)
- [NoMac service limits and documentation](https://nomac.app/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with CLI commands and MCP tool instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operational workflows for cloud Mac and iOS Simulator sessions, app builds, signing, and release.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
