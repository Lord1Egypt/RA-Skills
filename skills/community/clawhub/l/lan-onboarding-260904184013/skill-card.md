## Description:

Fast, safe first-run tour of the LAN CLI \u2014 discover networks, join a device network, message a peer, share files, and leave cleanly with verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to complete a first-run LAN CLI workflow: discover nearby networks, join one, exchange a message, share or retrieve files, verify each action, and leave cleanly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may install or run the LAN CLI from an untrusted source.

Mitigation: Install the LAN CLI only from a trusted source before starting the onboarding tour.

Risk: Users may join an unfamiliar local network or expose sensitive information through local-network messaging and file sharing.

Mitigation: Join only networks you recognize, do not send secrets, verify remote state after each action, and leave the network when finished.

## Reference(s):

- [LAN setup](references/setup.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a verification loop and safety guidance for local-network messaging and file sharing.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
