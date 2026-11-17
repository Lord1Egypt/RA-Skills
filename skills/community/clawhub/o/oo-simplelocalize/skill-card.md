## Description:

Operate SimpleLocalize through an OOMOL-connected account for reading, creating, updating, and deleting localization data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and localization teams use this skill to inspect SimpleLocalize projects, languages, translation keys, and translations, and to create, update, or delete localization data through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can install or update other agent skills without this skill explaining those changes.

Mitigation: Review the CLI's broader installation effects before proceeding, prefer a vetted fixed CLI release, consider setting OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization, and review any skills added during installation.

Risk: The remote installers and deployed connector implementation were not inspected, so their exact behavior remains uncertain; requests use OOMOL handling and connected credentials.

Mitigation: Review the CLI's broader installation effects before proceeding and ensure you accept OOMOL handling your SimpleLocalize requests and connected credentials.

## Reference(s):

- [SimpleLocalize](https://simplelocalize.io)
- [SimpleLocalize API documentation](https://api.simplelocalize.io/openapi/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Text]

**Output Format:** [JSON connector requests and responses, shell command examples, and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, create, update, or delete SimpleLocalize data; write and destructive actions require confirmation according to the skill.]

## Skill Version(s):

1.0.4 (source: evidence.json release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
