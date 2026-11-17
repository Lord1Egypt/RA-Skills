## Description:

Deploy an automated release management pipeline with 3 agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to configure a three-agent release workflow for changelog generation, semantic version coordination, and release announcements across approved channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs unpinned dependency skills for each agent role.

Mitigation: Review the named dependency skills and pin approved versions where possible before installation.

Risk: The setup creates persistent local setup state in ~/.pilot/setups/release-management.json.

Mitigation: Review the generated manifest before writing it and use a simple hostname-safe prefix.

Risk: The setup establishes agent trust relationships and can send release data to external services.

Mitigation: Verify peer identities before handshakes and restrict Slack, webhook, and email destinations to approved release channels with non-sensitive content.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-release-management-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, dependency skills for each role, and a running daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
