## Description:

Control D (controld.com) skill for reading, creating, updating, and deleting Control D data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents manage Control D profiles, service catalogs, and root-folder DNS rules through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include remote CLI installation, while installer and server-side connector behavior are unverified.

Mitigation: Review setup first, install a verified pinned CLI release yourself, and review automatic skill synchronization.

Risk: DNS rule changes can create, replace, or delete settings.

Mitigation: Keep explicit user approval for DNS changes and confirm the target and effect before acting.

## Reference(s):

- [Control D homepage](https://controld.com)
- [Control D API documentation](https://docs.controld.com/reference/get-started)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and concise Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Control D profile and DNS rule actions; write operations require user approval.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
