## Description:

Searches the iTunes Store and Apple Books Store and looks up records through the iTunes Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search iTunes and Apple Books catalog content or look up records by identifier through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions include installer downloads whose payloads have not been verified.

Mitigation: Review and approve CLI installation separately before running an installer.

Risk: Automatic bundled-skill synchronization could make broader changes across agent installations.

Mitigation: Disable automatic synchronization unless those changes are intended.

Risk: The hosted connector implementation is unverified, and use may involve OOMOL account charges.

Mitigation: Confirm the OOMOL account and possible charges before use.

## Reference(s):

- [iTunes Search API documentation](https://performance-partners.apple.com/search-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON catalog results and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: artifact frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
