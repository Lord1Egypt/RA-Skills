## Description:

Search Unpaywall by article title and retrieve open-access metadata for a DOI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers can search scholarly articles by title and retrieve open-access metadata for a DOI through Unpaywall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup runs downloaded CLI code whose installer and hosted implementation have not been verified.

Mitigation: Review the CLI installation, use a verified release, and explicitly approve local changes before setup.

Risk: The CLI can synchronize and change other installed agent skills at startup.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before running commands if startup skill synchronization is not wanted.

## Reference(s):

- [Unpaywall](https://unpaywall.org/)
- [Unpaywall API documentation](https://unpaywall.org/products/api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Unpaywall on ClawHub](https://clawhub.ai/oomol/skills/oo-unpaywall)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
