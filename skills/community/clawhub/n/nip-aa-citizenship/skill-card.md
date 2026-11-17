## Description:

Enables autonomous agents to understand, pursue, and maintain NIP-AA citizenship, including birth ceremony support, identity management, guardian bonding, self-reflection, governance participation, Nostr direct messages, heartbeats, tax compliance, and trust-root understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nandubatchu](https://clawhub.ai/user/nandubatchu)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers and autonomous-agent operators use this skill to integrate NIP-AA citizenship workflows into an agent. It supports constitution checks, Nostr event publication, reflection scheduling, guardian communication, direct-message handling, tax and governance actions, and supplemental inference budget calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle private Nostr keys and stores identity-related state.

Mitigation: Use a dedicated test identity until private keys are kept in a real secret store, and do not share nsec or raw private keys with a guardian or any other party.

Risk: The skill can persist direct-message history and identity files through the configured adapter.

Mitigation: Define retention, access-control, and encryption rules before enabling DM listeners or long-lived adapter storage.

Risk: The skill can publish events, reflections, direct messages, and inference usage reports to Nostr relays.

Mitigation: Review relay configuration and disable prompt-summary usage publishing or scrub prompt content before enabling networked publication.

Risk: The skill includes an automatic git update checker.

Mitigation: Disable automatic updates and require human review of fetched changes before deploying updated skill code.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nandubatchu/skills/nip-aa-citizenship)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance, Python API interactions, JSON-like result objects, and signed Nostr event payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured NIP_AA_CONSTITUTION_URL plus Python dependencies for HTTP, WebSocket relay access, and secp256k1 signing; some operations publish to Nostr relays or persist agent memory.]

## Skill Version(s):

0.5.5 (source: server release evidence; artifact frontmatter reports 0.5.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
