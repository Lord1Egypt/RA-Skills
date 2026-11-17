## Description:

nihao is a Nostr identity setup and health-check CLI that creates a complete Nostr identity and audits existing npub health with an agent-friendly Go binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dergigi](https://clawhub.ai/user/dergigi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and run a Nostr identity CLI for creating agent identities, publishing profile and wallet-related events, checking npub health, and exporting identity event backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the skill can create and publish a public Nostr identity immediately.

Mitigation: Review the skill before installation and use it only when a public Nostr identity should be created.

Risk: The generated nsec private key can be exposed or lost if it is handled insecurely.

Mitigation: Choose a secure nsec file location or password-manager command, avoid passing raw nsec values as command-line arguments, and back up the key.

Risk: Using go install with @latest fetches upstream source at install time.

Mitigation: Pin or review the upstream Go source before installation when supply-chain control is required.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to run a Go install command and produce or parse nihao JSON output.]

## Skill Version(s):

0.13.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
