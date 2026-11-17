## Description:

Fast, safe first-run tour of the LAN CLI: discover networks, join a device network, message a peer, share files, and leave cleanly with verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and new LAN CLI users use this skill to complete a first-run local network tour: discover networks, join one, exchange a message or file, verify results, and leave cleanly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the LAN CLI from an untrusted source could compromise the local system.

Mitigation: Install the LAN CLI only from a trusted source before following the onboarding steps.

Risk: Joining unrecognized LAN networks can expose the user to unintended local peers and traffic.

Mitigation: Join only networks you recognize and leave the network when the tour is complete.

Risk: Messages and shared files may be visible to every member of the LAN network.

Mitigation: Do not send secrets or sensitive files, and verify intended state with LAN CLI read-back commands.

## Reference(s):

- [LAN setup](references/setup.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides read-back verification after each LAN network action.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
