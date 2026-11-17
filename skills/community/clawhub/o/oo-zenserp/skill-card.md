## Description:

Zenserp (zenserp.com). Use this skill for ANY Zenserp request — searching and reading data. Whenever a task involves Zenserp, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Google Search, Images, Maps, and News through their connected Zenserp account and read the returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code without clear user approval.

Mitigation: Review and approve CLI setup separately; prefer a pinned, verified installation and check whether bundled-skill synchronization should be disabled.

Risk: Search inputs pass through OOMOL, and connected-account access requires trusting that service.

Mitigation: Review the service and account connection before using the skill with sensitive searches.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/oomol/skills/oo-zenserp)
- [Zenserp](https://zenserp.com)
- [Zenserp API documentation](https://app.zenserp.com/documentation)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON search results with textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by selected search action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
