## Description:

Search and read content in a user's connected Document360 account through OOMOL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Document360 account can search workspace content, list workspaces and articles, and inspect category hierarchies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code and make persistent agent changes without clear approval.

Mitigation: Use a separately reviewed, version-controlled CLI installation and require approval for setup changes. Review or disable managed-skill synchronization with the documented OO_SKILLS_SYNC_DISABLED control.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Document360](https://document360.com)
- [Document360 API documentation](https://apidocs.document360.com/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON connector requests and results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action input fields depend on the selected connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
