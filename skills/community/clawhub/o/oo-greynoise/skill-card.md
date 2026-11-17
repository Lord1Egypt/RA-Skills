## Description:

Search and read GreyNoise data, including looking up IPv4 addresses in the Community dataset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents investigating IP addresses can look up IPv4 addresses in GreyNoise Community and review whether they are known internet background noise, benign services, or classified activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs unverified remote code and may make broader changes to installed agent skills.

Mitigation: Review the installer and its skill changes before enabling this skill; prefer a verified, pinned release and confirm whether OO_SKILLS_SYNC_DISABLED is supported.

Risk: IP addresses submitted for lookup pass through OOMOL to GreyNoise.

Mitigation: Submit only addresses you are permitted to share, following your organization's data handling rules.

## Reference(s):

- [GreyNoise](https://www.greynoise.io)
- [GreyNoise Community API Documentation](https://docs.greynoise.io/docs/using-the-greynoise-community-api)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Text or Markdown summary of GreyNoise lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results depend on GreyNoise Community data and may be subject to per-source-IP throttling.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
