## Description:

Social awareness for AI entities: contacts, trust tiers, and identity verification over Nostr.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use NostrSocial to give agents a persistent Nostr-backed social graph for contact tiers, identity verification, conversation context, and relationship maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-run example exports and prints the root device secret used for proxy npub derivation.

Mitigation: Do not print or log exported secrets; store the device secret only in a secure secret manager, encrypted backup, or equivalent protected storage.

Risk: Use with real Nostr identities or contacts may expose sensitive identity, relationship, or relay data if configured casually.

Mitigation: Review the skill before installation, use pinned and reviewed package versions, and keep NOSTR_NSEC and NOSTRKEY_PASSPHRASE out of logs and source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vveerrgg/skills/nostrsocial)
- [Source homepage](https://github.com/HumanjavaEnterprises/nostrsocial.app.OC-python.src)
- [PyPI package](https://pypi.org/project/nostrsocial/)
- [NostrKey prerequisite](https://clawhub.ai/vveerrgg/nostrkey)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Python package setup, optional environment variables, contact-management examples, identity-verification examples, and trust-tier behavior guidance.]

## Skill Version(s):

0.1.3 (source: frontmatter, artifact metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
