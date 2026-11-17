## Description:

Look up GenderAPI.io data by email address, first name, or username through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the connected GenderAPI.io service to request likely gender lookups for an email address, first name, or username.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CLI installation runs remote code.

Mitigation: Review the CLI installation separately and use a verified release.

Risk: The CLI may change other installed agent skills at startup.

Mitigation: For connector-only use, set OO_SKILLS_SYNC_DISABLED=1 before invoking oo.

Risk: Lookup requests may contain email addresses, names, or usernames.

Mitigation: Submit only identifiers you are authorized to share with OOMOL and GenderAPI.io.

## Reference(s):

- [GenderAPI.io](https://www.genderapi.io)
- [GenderAPI.io API documentation](https://www.genderapi.io/api-documentation)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON lookup responses with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields depend on the selected lookup action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
