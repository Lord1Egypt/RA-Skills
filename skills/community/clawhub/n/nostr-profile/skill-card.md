## Description:

Nostr profile management for AI agents: publish, read, and update kind 0 metadata on any relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help an agent create, publish, read, and update public Nostr kind 0 profile metadata tied to an existing Nostr identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or update public Nostr profile metadata, making names, bios, image URLs, NIP-05 identifiers, and website links visible on public relays.

Mitigation: Confirm public profile content with the operator before publishing and avoid putting private or sensitive information in profile fields.

Risk: Profile publishing requires signing credentials, and the release security summary flags raw-key example risk.

Mitigation: Prefer the encrypted .nostrkey flow, do not display or log nsec values, and avoid placing raw nsec secrets in environment variables.

Risk: Third-party avatar services seeded with an npub can reveal a stable public identifier to that service.

Mitigation: Use self-hosted or operator-provided HTTPS image URLs when the privacy tradeoff of generated external image URLs is not acceptable.

Risk: The security guidance notes under-scoped dependency risk.

Mitigation: Install in an isolated environment and pin or audit Python dependencies before operational use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/vveerrgg/skills/nostr-profile)
- [Project homepage](https://github.com/HumanjavaEnterprises/huje.nostrprofile.OC-python.src)
- [PyPI package](https://pypi.org/project/nostr-profile/)
- [NostrKey prerequisite](https://clawhub.ai/vveerrgg/nostrkey)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python code examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce profile field values, relay choices, and Python snippets for publishing or reading public Nostr profile metadata.]

## Skill Version(s):

0.2.0 (source: evidence release, skill frontmatter, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
