## Description:

Helps users publish travelogues and photos to PowPow and create chat-capable digital humans pinned to its public map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow users use this skill to draft and publish travel posts with chosen photos and locations, or to create chat-capable digital humans on the public map. It also helps them preview and verify posts before and after publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a PowPow password in chat and caches a temporary account session token locally.

Mitigation: Use only if comfortable sharing credentials with the assistant; protect the local session and clear it when done.

Risk: Published posts, uploaded images, and selected locations can become public, including sensitive personal details.

Mitigation: Review the full preview, images, and map location before confirming; avoid private photos and home or work locations.

Risk: Authenticated actions can publish or delete posts and create digital humans that spend PowPow badges; scripts do not enforce confirmation themselves.

Mitigation: Require explicit approval for each publishing, deletion, or badge-spending action and verify the result afterward.

## Reference(s):

- [PowPow Simple EN on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-simple-en)
- [PowPow](https://global.powpow.online)
- [Skill security notes](references/security.md)
- [Skill screenshots](references/screenshots.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational text and Markdown with post drafts, previews, and publishing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can publish posts or digital humans to PowPow after explicit user confirmation; post results include a link and selected location.]

## Skill Version(s):

1.0.1 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
