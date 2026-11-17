## Description:

Uploadcare (uploadcare.com). Use this skill for ANY Uploadcare request — reading, creating, updating, and deleting data. Whenever a task involves Uploadcare, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Uploadcare files, groups, and project details, store files permanently, or delete files through their connected Uploadcare account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run a remote installer whose contents have not been verified.

Mitigation: Review and approve CLI installation separately; prefer a reviewed, version-pinned installer with integrity verification.

Risk: Connecting Uploadcare grants OOMOL access through the user's account.

Mitigation: Retain the skill's confirmation requirements for storing or deleting files.

## Reference(s):

- [Uploadcare API documentation](https://uploadcare.com/docs/api/)
- [Uploadcare](https://uploadcare.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell commands, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results use the connected Uploadcare account; storing and deleting files require confirmation of the exact action and target.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
