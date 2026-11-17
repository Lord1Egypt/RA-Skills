## Description:

Helps users turn travel photos and notes into public PowPow posts and create conversational digital humans pinned to a public map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow account holders use this skill to draft and publish travel stories with selected photos and locations, or create conversational digital humans on the public map. It also helps verify posts and remove the user's own test posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent requests a PowPow password and stores a session token locally.

Mitigation: Review the login request before use, protect the session directory, and clear the stored session when finished.

Risk: Scripts can upload local images, publish public posts, and delete the user's posts without enforced confirmation gates.

Mitigation: Confirm the account, exact draft, selected images, and location before publishing or deleting; provide only intended local files.

Risk: Creating a public digital human spends two non-refundable badges.

Mitigation: Confirm the character, public placement, account, and badge cost before creation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durenzidu/skills/powpow-simple-vi)
- [PowPow website](https://global.powpow.online)
- [Security and platform API reference](references/security.md)
- [Product screenshots](references/screenshots.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Conversational text, Markdown, and local HTML post drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can publish public posts and map-pinned digital humans through the user's PowPow account.]

## Skill Version(s):

1.0.2 (source: ClawHub release, skill frontmatter and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
