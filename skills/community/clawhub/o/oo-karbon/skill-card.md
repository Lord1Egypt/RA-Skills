## Description:

Search and read Karbon client groups, contacts, organizations, and tenant settings through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Karbon users can search for and read client groups, contacts, organizations, and tenant settings from an already connected Karbon account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions run a remotely downloaded installer, and scanner coverage was partial; the installer itself was not assessed.

Mitigation: Before installing, verify the installer source and contents, decide whether the CLI is needed, and review the referenced paths that were not covered by the scan.

## Reference(s):

- [Karbon API documentation](https://developers.karbonhq.com/)
- [Karbon homepage](https://karbonhq.com/)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [Karbon ClawHub release](https://clawhub.ai/oomol/skills/oo-karbon)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned records depend on the requested Karbon read action and connected account access.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
