## Description:

Search ContactOut and retrieve company, people, profile, and contact details through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search ContactOut for people and companies, find decision makers, enrich profiles, and check or verify contact details using identifiers such as LinkedIn URLs, email addresses, and company domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a remote installer that was unavailable for inspection, and CLI startup synchronization can change other installed agent skills.

Mitigation: Review and install the CLI separately before use; set OO_SKILLS_SYNC_DISABLED=1 to disable the documented startup synchronization.

Risk: ContactOut lookups send their identifiers to OOMOL and ContactOut and may incur usage charges.

Mitigation: Share only identifiers you intend those services to receive, and consider usage charges before running lookups.

## Reference(s):

- [ContactOut API documentation](https://api.contactout.com/)
- [ContactOut](https://contactout.com)
- [OOMOL oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [ContactOut lookup results and operating guidance as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain professional contact information returned by ContactOut.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
