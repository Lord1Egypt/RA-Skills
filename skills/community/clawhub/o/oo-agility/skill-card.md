## Description:

Search and read Agility CMS content, pages, sitemaps, and content models through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve Agility CMS content items, lists, pages, sitemaps, and content models from a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run remote installers whose release integrity was not verified.

Mitigation: Install a verified oo CLI release yourself before enabling the skill.

Risk: Managed skill synchronization may introduce broader agent changes without clear user control.

Mitigation: Review and approve skill changes; consider disabling managed-skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: The connected Agility CMS account may expose more content than a task requires.

Mitigation: Connect only the intended account and use read-only permissions where available.

## Reference(s):

- [Agility CMS Content Fetch API documentation](https://agilitycms.com/docs/developers/content-fetch-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured CMS data with text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
