## Description:

Search Scopus and retrieve document, author, affiliation, abstract, and source records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and other Scopus users use this skill to search Scopus and retrieve document, author, affiliation, abstract, and source records through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags automatic setup that runs unpinned remote code and can introduce changes to other agents’ skills.

Mitigation: Review and install a verified oo CLI release before use, consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1, and connect only the intended Scopus account.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Scopus](https://www.scopus.com/)
- [Scopus API documentation](https://dev.elsevier.com/sc_apis.html)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured Scopus responses as JSON, with textual summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieved content depends on the selected Scopus action and connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
