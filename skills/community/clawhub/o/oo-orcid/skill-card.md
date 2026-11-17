## Description:

ORCID (orcid.org). Use this skill for ANY ORCID request — searching and reading data. Whenever a task involves ORCID, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and assistants use this skill to search public ORCID records and read a researcher's public profile or works through a connected ORCID account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may lead an agent to run a downloaded installer without a clear approval step.

Mitigation: Use a separately verified oo CLI installation and require approval before downloading or executing installers; check whether setup will install or update other agent skills.

## Reference(s):

- [ORCID](https://orcid.org/)
- [ORCID API documentation](https://info.orcid.org/documentation/api-tutorials/api-tutorial-get-and-authenticated-orcid-id/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ORCID ClawHub release](https://clawhub.ai/oomol/skills/oo-orcid)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Public ORCID record, works summary, or search results returned as structured data and presented as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action and are limited to public ORCID data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
