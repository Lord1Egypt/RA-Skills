## Description:

Search and read Breeze data through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to search and read people, profile fields, tags, and tag folders in Breeze through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the user to execute downloaded installer code whose contents are unverified.

Mitigation: If installation is needed, use a separately reviewed, version-pinned CLI and require approval before running its installer.

Risk: The connected account exposes personal records through OOMOL, and the CLI may synchronize additional skills.

Mitigation: Connect only the intended Breeze account and review the CLI's additional skill synchronization behavior.

## Reference(s):

- [Breeze API documentation](https://www.breezechms.com/api)
- [Breeze homepage](https://www.breezechms.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON connector requests and responses with natural-language task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector response fields vary by Breeze action; actions documented by this skill are read-only.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
