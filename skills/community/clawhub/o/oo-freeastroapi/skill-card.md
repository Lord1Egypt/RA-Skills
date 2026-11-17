## Description:

This skill lets agents search and retrieve FreeAstroAPI data through the OOMOL-connected oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search and retrieve astrology, astronomy, calendar, and location data from FreeAstroAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup downloads code, and automatic skill synchronization may make persistent changes in other agent apps.

Mitigation: Review and install the CLI separately, checking its release and local changes; disable automatic skill synchronization if it is not needed.

Risk: Birth details and other submitted information are processed by OOMOL and FreeAstroAPI.

Mitigation: Share only the names and birth details intended for those services to process.

## Reference(s):

- [FreeAstroAPI](https://www.freeastroapi.com/)
- [FreeAstroAPI documentation](https://www.freeastroapi.com/zh/docs)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields vary by action; responses include data and execution metadata.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
