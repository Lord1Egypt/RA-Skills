## Description:

Helps users draft and publish travel stories on PowPow and create conversational digital humans pinned to its public map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

PowPow account holders use this Japanese-language skill to turn photos and notes into travel posts, publish them to PowPow, and create chat-enabled digital humans on a public map. The assistant can draft content, suggest locations and images, and verify published posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The assistant handles PowPow login credentials and a stored session.

Mitigation: Use a dedicated account if possible and remove the stored session from POWPOW_STATE_DIR when finished.

Risk: Publishing, uploading, or deleting content can change the user's public account.

Mitigation: Review the account, exact draft, and images before approving any publish or delete action.

Risk: Map pins can publicly disclose a location, and creating a digital human can spend account badges.

Mitigation: Confirm the map location and badge cost before creating or publishing a digital human.

## Reference(s):

- [PowPow Simple JA on ClawHub](https://clawhub.ai/durenzidu/skills/powpow-simple-ja)
- [PowPow website](https://global.powpow.online)
- [Skill security documentation](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [Text, HTML, API calls]

**Output Format:** [Conversational text, formatted post drafts, and published PowPow content and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PowPow account; publishing and digital-human creation affect the user's public account.]

## Skill Version(s):

1.0.2 (source: ClawHub release, skill frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
