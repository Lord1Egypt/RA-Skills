## Description:

Helps users turn photos into travelogues, publish them to PowPow, and create chat-capable digital humans pinned to its public map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow account holders use this skill to draft and publish photo-based travel stories and create map-pinned digital humans. It can help select locations and images, preview posts, and verify published results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable session token can authorize publishing, image uploads, digital-human creation, and post deletion without an enforced confirmation gate.

Mitigation: Require a visible preview and explicit user approval before publishing, creating a digital human, or deleting a post.

Risk: An agent handling account credentials and a stored login token could expose the account if local state is accessible to others.

Mitigation: Confirm the state configuration points to the official PowPow site and protect or delete ~/.powpow/session.json on shared machines.

Risk: Publishing a post or digital human may expose photos and locations publicly; digital-human creation consumes badges.

Mitigation: Review the intended content, images, map location, and badge cost with the user before approval.

## Reference(s):

- [PowPow Publisher on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-publisher)
- [PowPow website](https://global.powpow.online)
- [PowPow public map](https://global.powpow.online/map)
- [Skill security notes](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational text and Markdown drafts, previews, and publication links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can publish public posts and map-pinned digital humans; reports publication results and links.]

## Skill Version(s):

1.0.5 (source: frontmatter, ClawHub release, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
